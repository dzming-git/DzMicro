import yaml
from dzmicro.utils import WatchDogThread, consul_client

class ConsulInfo:
    _config_path = ''
    _watch_dog = None

    @classmethod
    def load_config(cls, config_path, reload_flag=False):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

            token = config.get('TOKEN', '')
            consul_client.set_token(token)

            kvs = config.get('KV', {})
            for kv in kvs:
                consul_client.update_key_value(kv)

            if not reload_flag:
                cls._config_path = config_path
                cls._watch_dog = WatchDogThread(config_path, cls.reload_config)
                cls._watch_dog.start()

    @classmethod
    def reload_config(cls):
        cls.load_config(config_path=cls._config_path, reload_flag=True)
