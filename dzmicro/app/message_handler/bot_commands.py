# bot_commands.py
import threading
from typing import List

class BotCommands:
    def __init__(self, uuid: str, is_platform: bool = False) -> None:

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
        self._bot_commands = {}
        self._lock = threading.Lock()
        self.uuid = uuid
        self.is_platform = is_platform

    def add_keyword(self, keyword: str, service_name: str) -> None:
        with self._lock:
            self._bot_commands[keyword] = {}
            self._bot_commands[keyword]['service_name'] = service_name
            self._bot_commands[keyword]['command'] = []

    def add_commands(self, keyword: str, command: str) -> None:
        with self._lock:
            if keyword in self._bot_commands:
                self._bot_commands[keyword]['command'].append(command)
                print(self._bot_commands)
            else:
                print('请先添加keyword')
    
    def get_keywords(self) -> List[str]:
        with self._lock:
            return list(self._bot_commands.keys())
    
    def get_commands(self, keyword: str) -> List[str]:
        with self._lock:
            return self._bot_commands.get(keyword, {}).get('command', [])
    
    def get_service_name(self, keyword: str) -> str:
        with self._lock:
            return self._bot_commands.get(keyword, {}).get('service_name', '')
    