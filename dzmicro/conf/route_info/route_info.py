# route_info.py
import yaml
import copy
from dzmicro.utils import WatchDogThread, compare_dicts
from typing import List
from dzmicro.utils.singleton import singleton

@singleton
class RouteInfo:
    def __init__(self) -> None:
        self._config_path = ''
        self._config = {}
        self._watch_dog = None
        self._service_conf = {}

    def load_config(self, config_path: str, reload_flag: bool = False) -> None:
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
            self._service_conf = self._config.get('service', {})
            if not reload_flag:
                self._config_path = config_path
                self._watch_dog = WatchDogThread(config_path, self.reload_config)
                self._watch_dog.start()

    def reload_config(self) -> None:
        config_old = copy.deepcopy(self._config)
        self.load_config(config_path=self._config_path, reload_flag=True)
        config_new = copy.deepcopy(self._config)
        added_dict, deleted_dict, modified_dict = compare_dicts(config_old, config_new)
        if added_dict or deleted_dict or modified_dict:
            from dzmicro.app import server_thread
            server_thread.restart()

    # 服务程序配置方法
    def get_service_name(self) -> str:
        return self._service_conf.get('name', '')

    def get_service_ip(self) -> str:
        return self._service_conf.get('ip', '')

    def get_service_port(self) -> str:
        return self._service_conf.get('port', '')

    def get_service_tags(self) -> List[str]:
        return self._service_conf.get('tags', [])
    