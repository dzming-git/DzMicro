class FuncDict:
    _func_dict = {}

    @classmethod
    def set_func_dict(cls, func_dict):
        cls._func_dict = func_dict
    
    @classmethod
    def get_commands(cls):
        return list(cls._func_dict.keys())
    
    @classmethod
    def get_func(cls, command):
        return cls._func_dict.get(command).get('func')
    
    @classmethod
    def get_permission(cls, command):
        return cls._func_dict.get(command).get('permission')