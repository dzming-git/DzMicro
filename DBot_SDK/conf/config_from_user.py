class ConfigFromUser:
    _is_platform = False

    @classmethod
    def is_platform(cls, confirm=None):
        '''
        查询/确认是否是平台程序程序
        confirm参数不输入时为查询
        '''
        if confirm:
            cls._is_platform = True
            return True
        else:
            return cls._is_platform
    
    @classmethod
    def Authority_load_config(cls, config_path):
        from DBot_SDK.conf import Authority
        Authority.load_config(config_path)
    
    @classmethod
    def RouteInfo_load_config(cls, config_path):
        from DBot_SDK.conf import RouteInfo
        RouteInfo.load_config(config_path)
    
    @classmethod
    def ConsulInfo_load_config(cls, config_path):
        from DBot_SDK.conf import ConsulInfo
        ConsulInfo.load_config(config_path)
    
    @classmethod
    def set_func_dict(cls, func_dict):
        from DBot_SDK.app import FuncDict
        FuncDict.set_func_dict(func_dict)
    
    @classmethod
    def set_keyword(cls, keyword):
        from DBot_SDK.app import FuncDict
        FuncDict.set_keyword(keyword)

