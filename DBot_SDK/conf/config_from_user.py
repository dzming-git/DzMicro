class ConfigFromUser:
    @classmethod
    def Authority_load_config(cls, config_path):
        from DBot_SDK.conf import Authority
        Authority.load_config(config_path)
    
    @classmethod
    def RouteInfo_load_config(cls, config_path):
        from DBot_SDK.conf import RouteInfo
        RouteInfo.load_config(config_path)
    
    @classmethod
    def set_server_name(cls, server_name):
        from DBot_SDK.app import server_thread
        server_thread.set_server_name(server_name)
    
    @classmethod
    def set_func_dict(cls, func_dict):
        from DBot_SDK.app import FuncDict
        FuncDict.set_func_dict(func_dict)
