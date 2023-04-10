import yaml
from dzmicro.utils import WatchDogThread
from typing import List, Dict

class ConsulInfo:
    def __init__(self, uuid: str, is_platform: bool = False) -> None:
        self._config_path = ''
        self._watch_dog = None
        self.uuid = uuid
        self.is_platform = is_platform
        self.token = ''
        self.prefix = ''
        self.kvs = {}

    def load_config(self, config_path: str, reload_flag: str = False) -> None:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

            self.token = config.get('TOKEN', '')
            self.prefix = config.get('PREFIX', '')
            self.kvs = config.get('KV', [])

            if not reload_flag:
                self._config_path = config_path
                self._watch_dog = WatchDogThread(config_path, self.reload_config)
                self._watch_dog.start()

    def reload_config(self) -> None:
        self.load_config(config_path=self._config_path, reload_flag=True)
    
    def get_token(self) -> str:
        return self.token

    def get_prefix(self) -> str:
        return self.prefix
    
    def get_kvs(self) -> List[Dict[str, str]]:
        return self.kvs
