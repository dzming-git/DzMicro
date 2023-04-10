import yaml
from dzmicro.utils import WatchDogThread
from typing import Tuple

class MQInfo:
    def __init__(self, uuid: str, is_platform: bool = False) -> None:
        self._config = {}
        self._config_path = ''
        self._watch_dog = None
        self.uuid = uuid
        self.is_platform = is_platform

    def load_config(self, config_path: str, reload_flag: str = False) -> None:
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
            if not reload_flag:
                self._config_path = config_path
                self._watch_dog = WatchDogThread(config_path, self.reload_config)
                self._watch_dog.start()

    def reload_config(self) -> None:
        self.load_config(config_path=self._config_path, reload_flag=True)
    
    def get_uesrinfo(self) -> Tuple[str, str]:
        username = self._config.get('USERNAME', '')
        password = self._config.get('PASSWORD', '')
        return username, password
