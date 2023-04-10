# message_sender.py
from typing import List, Dict, Callable, Union

class MessageSender:
    def __init__(self, uuid: str, is_platform: bool = False) -> None:
        self.send_message_to_source: Callable[[str, List, bool], None] = None
        self._mq = None
        self.uuid = uuid  
        self.is_platform = is_platform
        
    def set_server_unique_info(self) -> None:
        from dzmicro.utils import singleton_server_manager
        self.server_unique_info = singleton_server_manager.get_server_unique_info(self.uuid)

    def send_message_to_platform(self, message: str, source_id: List[any]):
        correlation_id = self.server_unique_info.producer_mq.send_task({'message': message, 'source_id': source_id}, 'service_message')
        reply = self.server_unique_info.mq_replay_thread.wait_reply(correlation_id, {'message': message, 'source_id': source_id}, 'service_message', True)
        if reply is None:
            print('连接平台超时')
    
    def set_send_message_to_source(self, func: Callable[[str, List, bool], None]) -> None:
        self.send_message_to_source = func
