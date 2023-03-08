class FuncDict:
    _func_dict = {}

    @classmethod
    def set_func_dict(cls, func_dict):
        cls._func_dict = func_dict
    
    @classmethod
    def get_func_dict(cls):
        return cls._func_dict