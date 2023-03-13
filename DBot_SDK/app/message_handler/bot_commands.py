# bot_commands.py
import threading

class BotCommands:
    _bot_commands = {}
    _lock = threading.Lock()

    @classmethod
    def add_commands(cls, command, service_name):
        with cls._lock:
            cls._bot_commands[command] = service_name
            print(cls._bot_commands)
    
    @classmethod
    def get_commands(cls):
        with cls._lock:
            return list(cls._bot_commands.keys())
    
    @classmethod
    def get_service_name(cls, command):
        with cls._lock:
            return cls._bot_commands[command]
    


