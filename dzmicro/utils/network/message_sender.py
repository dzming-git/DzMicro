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
        from dzmicro.utils.network import create_mq
        if self._mq is None:
            self._mq = create_mq()
        self._mq.send_task({'message': message, 'source_id': source_id}, 'service_message')
        # from dzmicro.utils.network import ConsulClient
        # consul_client = ConsulClient()
        # platform_name = consul_client.download_key_value('config/platform', '""')
        # if platform is None:
        #     platform = consul_client.discover_service(platform_name)
        # ip, port = platform
        # url = f'http://{ip}:{port}/api/v1/service_message'
        # response = requests.post(url, json={'message': message, 'source_id': source_id})
        # return response.json()
    
    def set_send_message_to_source(self, func: Callable[[str, List, bool], None]) -> None:
        self.send_message_to_source = func
