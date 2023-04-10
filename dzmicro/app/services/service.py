from typing import Dict, List, Optional, Callable

class FuncDict:
    def __init__(self, uuid: str, is_platform: bool = False) -> None:
        self._func_dict = {}
        self._keyword = ''
        self.uuid = uuid
        self.is_platform = is_platform

    def set_keyword(self, keyword: str) -> None:
        self._keyword = keyword

    def set_func_dict(self, func_dict: Dict[str, Dict[str, any]]) -> None:
        self._func_dict = func_dict
    
    def get_keyword(self) -> str:
        return self._keyword

    def get_commands(self) -> List[str]:
        return list(self._func_dict.keys())
    
    def get_func(self, command: str) -> Optional[Callable[[Dict[str, any]], None]]:
        return self._func_dict.get(command, {}).get('func')
    
    def get_permission(self, command: str) -> str:
        return self._func_dict.get(command, {}).get('permission')
