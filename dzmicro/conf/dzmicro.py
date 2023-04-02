from typing import List, Callable, Dict

class DzMicro:
    def __init__(self) -> None:
        self._is_platform = False

    def is_platform(self, confirm: bool = None) -> bool:
        '''
        查询/确认是否是平台程序程序
        confirm参数不输入时为查询
        设置成类方法，供全局查询
        '''
        if confirm:
            self._is_platform = True
        return self._is_platform
    
    def set_authority_config(self, config_path: str) -> None:
        from dzmicro.conf import Authority
        authority = Authority()
        authority.load_config(config_path)
    
    def set_route_info_config(self, config_path: str) -> None:
        from dzmicro.conf import RouteInfo
        route_info = RouteInfo()
        route_info.load_config(config_path)
    
    def set_consul_info_config(self, config_path: str) -> None:
        from dzmicro.conf import ConsulInfo
        consul_info = ConsulInfo()
        consul_info.load_config(config_path)
    
    def set_mq_info_config(self, config_path: str) -> None:
        from dzmicro.conf import MQInfo
        mq_info = MQInfo()
        mq_info.load_config(config_path)
    
    def set_func_dict(self, func_dict_input: Dict[str, Dict[str, any]]) -> None:
        from dzmicro.app import FuncDict
        func_dict = FuncDict()
        func_dict.set_func_dict(func_dict_input)
    
    def set_keyword(self, keyword: str) -> None:
        from dzmicro.app import FuncDict
        func_dict = FuncDict()
        func_dict.set_keyword(keyword)
    
    def set_send_message_to_source(self, func: Callable[[str, List, bool], None]) -> None:
        from dzmicro.utils.network import MessageSender
        message_sender = MessageSender()
        message_sender.set_send_message_to_source(func)

    def start_server(self, safe_start: bool = True) -> bool:
        from dzmicro.app import ServerThread
        server_thread = ServerThread()
        server_thread.set_safe_start(safe_start)
        return server_thread.start(self._is_platform)

    def start_consume(self) -> bool:
        if self._is_platform:
            from dzmicro.api.platform.platform_consumer import start_consume
        else:
            from dzmicro.api.server.server_consumer import start_consume
        self.mq_consumer = start_consume()
        return True

    def start(self) ->bool:
        return \
            self.start_server() and \
            self.start_consume()
