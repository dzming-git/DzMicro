class FuncDict:
    _func_dict = {}
    _keyword = ''

    @classmethod
    def set_keyword(cls, keyword):
        cls._keyword = keyword

    @classmethod
    def set_func_dict(cls, func_dict):
        cls._func_dict = func_dict
    
    @classmethod
    def get_keyword(cls):
        return cls._keyword

    @classmethod
    def get_commands(cls):
        return list(cls._func_dict.keys())
    
    @classmethod
    def get_func(cls, command):
        return cls._func_dict.get(command).get('func')
    
    @classmethod
    def get_permission(cls, command):
        return cls._func_dict.get(command).get('permission')