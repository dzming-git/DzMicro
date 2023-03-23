# route_info.py
import yaml
import copy
from dbot.utils import WatchDogThread, compare_dicts

class RouteInfo:
    _config_path = ''
    _config = {}
    _watch_dog = None
    _service_conf = {}

    @classmethod
    def load_config(cls, config_path, reload_flag=False):
        with open(config_path, 'r', encoding='utf-8') as f:
            cls._config = yaml.safe_load(f)
            cls._service_conf = cls._config.get('service', {})
            if not reload_flag:
                cls._config_path = config_path
                cls._watch_dog = WatchDogThread(config_path, cls.reload_config)
                cls._watch_dog.start()

    @classmethod
    def reload_config(cls):
        config_old = copy.deepcopy(cls._config)
        cls.load_config(config_path=cls._config_path, reload_flag=True)
        config_new = copy.deepcopy(cls._config)
        added_dict, deleted_dict, modified_dict = compare_dicts(config_old, config_new)
        if added_dict or deleted_dict or modified_dict:
            from dbot.app import server_thread
            server_thread.restart()

    # 服务程序配置方法
    @classmethod
    def get_service_name(cls):
        return cls._service_conf.get('name')

    @classmethod
    def get_service_ip(cls):
        return cls._service_conf.get('ip')

    @classmethod
    def get_service_port(cls):
        return cls._service_conf.get('port')

    @classmethod
    def get_service_tags(cls):
        return cls._service_conf.get('tags', [])
    