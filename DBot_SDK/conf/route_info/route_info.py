# route_info.py
import yaml
import copy
from DBot_SDK.utils import WatchDogThread, compare_dicts
from DBot_SDK.conf import ConfigFromUser

class RouteInfo:
    _is_platform = False
    _config_path = ''
    _config = {}
    _watch_dog = None
    _service_conf = {}
    _platform_find = False
    _platform_conf_from_file = {}
    _platform_conf_from_consul = {'endpoints': {}}

    @classmethod
    def load_config(cls, config_path, reload_flag=False):
        cls._is_platform = ConfigFromUser.is_platform()
        with open(config_path, 'r', encoding='utf-8') as f:
            cls._config = yaml.safe_load(f)
            cls._service_conf = cls._config.get('service', {})
            if cls._is_platform:
                cls._platform_find = True
            cls._platform_conf_from_file = cls._config.get('platform', {})
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
            from DBot_SDK.app import server_thread
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

    # 平台程序配置方法
    @classmethod
    def get_platform_name(cls):
        return cls._platform_conf_from_file.get('name')
    
    @classmethod
    def is_platform_find(cls):
        return cls._platform_find
    
    @classmethod
    def update_platform(cls, ip, port):
        cls._platform_find = True
        cls._platform_conf_from_consul['ip'] = ip
        cls._platform_conf_from_consul['port'] = port
    
    @classmethod
    def get_platform_ip(cls):
        if cls._is_platform:
            return cls._platform_conf_from_file.get('ip')
        if cls._platform_find:
            return cls._platform_conf_from_consul.get('ip')
        return None
    
    @classmethod
    def get_platform_port(cls):
        if cls._is_platform:
            return cls._platform_conf_from_file.get('port')
        if cls._platform_find:
            return cls._platform_conf_from_consul.get('port')
        return None
    
    @classmethod
    def get_platform_tags(cls):
        if cls._is_platform:
            return cls._platform_conf_from_file.get('tags')
        if cls._platform_find:
            return cls._platform_conf_from_consul.get('tags')
        return []
    
    @classmethod
    def get_platform_consul_key(cls, usage):
        return cls._platform_conf_from_file.get('consul_key')[usage]
