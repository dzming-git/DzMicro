from typing import List, Callable

class DzMicro:
    def __init__(self) -> None:
        from dzmicro.app import server_thread
        self._server_thread = server_thread
        self._is_platform = False

    def is_platform(self, confirm=None):
        '''
        查询/确认是否是平台程序程序
        confirm参数不输入时为查询
        设置成类方法，供全局查询
        '''
        if confirm:
            self._is_platform = True
            return True
        else:
            return self._is_platform
    
    def set_Authority_config(self, config_path):
        from dzmicro.conf import Authority
        Authority.load_config(config_path)
    
    def set_RouteInfo_config(self, config_path):
        from dzmicro.conf import RouteInfo
        RouteInfo.load_config(config_path)
    
    def set_ConsulInfo_config(self, config_path):
        from dzmicro.conf import ConsulInfo
        ConsulInfo.load_config(config_path)
    
    def set_func_dict(self, func_dict):
        from dzmicro.app import FuncDict
        FuncDict.set_func_dict(func_dict)
    
    def set_keyword(self, keyword):
        from dzmicro.app import FuncDict
        FuncDict.set_keyword(keyword)
    
    def set_send_message_to_source(self, func: Callable[[str, List, bool], None]):
        from dzmicro.utils.network import MessageSender
        MessageSender.set_send_message_to_source(func)

    def start_server(self, safe_start: bool = True) -> bool:
        self._server_thread.set_safe_start(safe_start)
        return self._server_thread.start(self._is_platform)
    
    def handle(self, message, source_id):
        from dzmicro.app.message_handler.message_handler import message_handler_thread
        message_handler_thread.message_handler(message, source_id)
