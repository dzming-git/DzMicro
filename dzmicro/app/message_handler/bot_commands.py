# bot_commands.py
import threading
from typing import List

class BotCommands:
    '''
    用于储存/查找 关键词、指令与服务名的映射关系

    例子：
    _bot_commands = {
        '#测试':{
            'service_name': 'test',
            'command':[
                'cmd1',
                'cmd2'
            ]
        }
    }
    '''
    _bot_commands = {}
    _lock = threading.Lock()

    @classmethod
    def add_keyword(cls, keyword: str, service_name: str) -> None:
        with cls._lock:
            cls._bot_commands[keyword] = {}
            cls._bot_commands[keyword]['service_name'] = service_name
            cls._bot_commands[keyword]['command'] = []

    @classmethod
    def add_commands(cls, keyword: str, command: str) -> None:
        with cls._lock:
            if keyword in cls._bot_commands:
                cls._bot_commands[keyword]['command'].append(command)
                print(cls._bot_commands)
            else:
                print('请先添加keyword')
    
    @classmethod
    def get_keywords(cls) -> List[str]:
        with cls._lock:
            return list(cls._bot_commands.keys())
    
    @classmethod
    def get_commands(cls, keyword: str) -> List[str]:
        with cls._lock:
            return cls._bot_commands.get(keyword, {}).get('command', [])
    
    @classmethod
    def get_service_name(cls, keyword: str) -> str:
        with cls._lock:
            return cls._bot_commands.get(keyword, {}).get('service_name', '')
    


