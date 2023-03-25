import yaml
from dzmicro.utils import WatchDogThread, ConsulClient
from dzmicro.utils.singleton import singleton

@singleton
class ConsulInfo:
    def __init__(self) -> None:
        self._config_path = ''
        self._watch_dog = None

    def load_config(self, config_path: str, reload_flag: str = False) -> None:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

            #TODO 放这里感觉有些不合适
            consul_client = ConsulClient()
            token = config.get('TOKEN', '')
            consul_client.set_token(token)
            prefix = config.get('PREFIX', '')
            consul_client.set_prefix(prefix)
            consul_client.start_watch_kv()

            kvs = config.get('KV', {})
            for kv in kvs:
                consul_client.update_key_value(kv)

            if not reload_flag:
                self._config_path = config_path
                self._watch_dog = WatchDogThread(config_path, self.reload_config)
                self._watch_dog.start()

    def reload_config(self) -> None:
        self.load_config(config_path=self._config_path, reload_flag=True)
