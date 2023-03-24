from typing import Dict, List, Optional, Callable

class FuncDict:
    _func_dict = {}
    _keyword = ''

    @classmethod
    def set_keyword(cls, keyword: str) -> None:
        cls._keyword = keyword

    @classmethod
    def set_func_dict(cls, func_dict: Dict[str, Dict[str, any]]) -> None:
        cls._func_dict = func_dict
    
    @classmethod
    def get_keyword(cls) -> str:
        return cls._keyword

    @classmethod
    def get_commands(cls) -> List[str]:
        return list(cls._func_dict.keys())
    
    @classmethod
    def get_func(cls, command: str) -> Optional[Callable[[Dict[str, any]], None]]:
        return cls._func_dict.get(command).get('func')
    
    @classmethod
    def get_permission(cls, command: str) -> str:
        return cls._func_dict.get(command).get('permission')