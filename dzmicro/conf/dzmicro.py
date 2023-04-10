from typing import List, Callable, Dict
from dzmicro.utils.server_manager import singleton_server_manager
import uuid

class DzMicro:
    def __init__(self, is_platform: bool = False) -> None:
        self.uuid = str(uuid.uuid4())
        self._is_platform = is_platform
        singleton_server_manager.add_server(self.uuid, is_platform)
    
    def set_authority_config(self, config_path: str) -> None:
        singleton_server_manager.servers[self.uuid].authority.load_config(config_path)
    
    def set_route_info_config(self, config_path: str) -> None:
        singleton_server_manager.servers[self.uuid].route_info.load_config(config_path)
    
    def set_consul_info_config(self, config_path: str) -> None:
        singleton_server_manager.servers[self.uuid].consul_info.load_config(config_path)
    
    def set_mq_info_config(self, config_path: str) -> None:
        singleton_server_manager.servers[self.uuid].mq_info.load_config(config_path)
    
    def set_func_dict(self, func_dict_input: Dict[str, Dict[str, any]]) -> None:
        singleton_server_manager.servers[self.uuid].func_dict.set_func_dict(func_dict_input)
    
    def set_keyword(self, keyword: str) -> None:
        singleton_server_manager.servers[self.uuid].func_dict.set_keyword(keyword)
    
    def set_send_message_to_source(self, func: Callable[[str, List, bool], None]) -> None:
        singleton_server_manager.servers[self.uuid].message_sender.set_send_message_to_source(func)

    def start(self, safe_start: bool = True) ->bool:
        singleton_server_manager.servers[self.uuid].server_thread.set_safe_start(safe_start)
        return singleton_server_manager.load_server(self.uuid)
