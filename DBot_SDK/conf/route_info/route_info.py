# route_info.py
import yaml
import copy
from DBot_SDK.utils import WatchDogThread, compare_dicts
from DBot_SDK.conf import ConfigFromUser

class RouteInfo:
    _is_message_broker = False
    _config_path = ''
    _config = {}
    _watch_dog = None
    _service_conf = {}
    _message_broker_find = False
    _message_broker_conf_from_file = {}
    _message_broker_conf_from_consul = {'endpoints': {}}

    @classmethod
    def load_config(cls, config_path, reload_flag=False):
        cls._is_message_broker = ConfigFromUser.is_message_broker()
        with open(config_path, 'r', encoding='utf-8') as f:
            cls._config = yaml.safe_load(f)
            if not cls._is_message_broker:
                cls._service_conf = cls._config.get('service', {})
            else:
                _message_broker_find = True
            cls._message_broker_conf_from_file = cls._config.get('message_broker', {})
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
        return cls._service_conf.get('tags')
    
    @classmethod
    def get_service_endpoints_info(cls):
        return cls._service_conf.get('endpoints')
    
    @classmethod
    def get_service_endpoint(cls, usage):
        return cls._service_conf.get('endpoints')[usage]

    # 消息代理配置方法
    @classmethod
    def get_message_broker_name(cls):
        return cls._message_broker_conf_from_file.get('name')
    
    @classmethod
    def is_message_broker_find(cls):
        return cls._message_broker_find
    
    @classmethod
    def update_message_broker(cls, ip, port):
        cls._message_broker_find = True
        cls._message_broker_conf_from_consul['ip'] = ip
        cls._message_broker_conf_from_consul['port'] = port
    
    @classmethod
    def get_message_broker_ip(cls):
        if cls._is_message_broker:
            return cls._message_broker_conf_from_file.get('ip')
        if cls._message_broker_find:
            return cls._message_broker_conf_from_consul.get('ip')
        return None
    
    @classmethod
    def get_message_broker_port(cls):
        if cls._is_message_broker:
            return cls._message_broker_conf_from_file.get('port')
        if cls._message_broker_find:
            return cls._message_broker_conf_from_consul.get('port')
        return None
    
    @classmethod
    def add_message_broker_endpoint(cls, usage, endpoint):
        cls._message_broker_conf_from_consul['endpoints'][usage] = endpoint
    
    @classmethod
    def get_message_broker_endpoints_info(cls):
        if cls._is_message_broker:
            return cls._message_broker_conf_from_file.get('endpoints')
        return cls._message_broker_conf_from_consul.get('endpoints')

    @classmethod
    def get_message_broker_endpoint(cls, usage):
        if cls._is_message_broker:
            return cls._message_broker_conf_from_file.get('endpoints')[usage]
        return cls._message_broker_conf_from_consul.get('endpoints')[usage]
    
    @classmethod
    def get_message_broker_consul_key(cls, usage):
        return cls._message_broker_conf_from_file.get('consul_key')[usage]
