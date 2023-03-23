class DBot:
    _is_platform = False

    def __init__(self) -> None:
        from dbot.app import server_thread
        self._server_thread = server_thread

    @classmethod
    def is_platform(cls, confirm=None):
        '''
        查询/确认是否是平台程序程序
        confirm参数不输入时为查询
        设置成类方法，供全局查询
        '''
        if confirm:
            cls._is_platform = True
            return True
        else:
            return cls._is_platform
    
    def set_authority_config(self, config_path):
        from dbot.conf import Authority
        Authority.load_config(config_path)
    
    def set_routeInfo_config(self, config_path):
        from dbot.conf import RouteInfo
        RouteInfo.load_config(config_path)
    
    def set_consulInfo_config(self, config_path):
        from dbot.conf import ConsulInfo
        ConsulInfo.load_config(config_path)
    
    def set_func_dict(self, func_dict):
        from dbot.app import FuncDict
        FuncDict.set_func_dict(func_dict)
    
    def set_keyword(self, keyword):
        from dbot.app import FuncDict
        FuncDict.set_keyword(keyword)

    def start_server(self, safe_start: bool = True) -> bool:
        self._server_thread.set_safe_start(safe_start)
        return self._server_thread.start()

