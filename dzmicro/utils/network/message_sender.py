# message_sender.py
import requests
from typing import List, Dict, Callable, Union
from dzmicro.utils.singleton import singleton

@singleton
class MessageSender:
    def __init__(self) -> None:
        self.send_message_to_source: Callable[[str, List, bool], None] = None
        self._mq = None
        

    def send_message_to_platform(self, message: str, source_id: List[any], platform: Union[List[List[str]], None] = None) -> Dict[str, any]:
        from dzmicro.utils.network.mq import create_mq, MQReplyThread
        if self._mq is None:
            self._mq = create_mq()
        correlation_id = self._mq.send_task({'message': message, 'source_id': source_id}, 'service_message')
        mq_reply = MQReplyThread()
        reply = mq_reply.wait_reply(correlation_id, {'message': message, 'source_id': source_id}, 'service_message', True)
        if reply is None:
            print('连接平台超时')
    
    def set_send_message_to_source(self, func: Callable[[str, List, bool], None]) -> None:
        self.send_message_to_source = func
