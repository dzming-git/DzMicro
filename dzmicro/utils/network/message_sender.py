# message_sender.py
import requests
from typing import List, Callable

class MessageSender:
    send_message_to_source: Callable[[str, List, bool], None] = None

    @classmethod
    def send_message_to_platform(cls, message, source_id, platform=None):
        from dzmicro.utils.network import consul_client
        platform_name = consul_client.download_key_value('config/platform', '""')
        if platform is None:
            platform = consul_client.discover_service(platform_name)
        ip, port = platform
        url = f'http://{ip}:{port}/api/v1/service_message'
        response = requests.post(url, json={'message': message, 'source_id': source_id})
        return response.json()
    
    @classmethod
    def set_send_message_to_source(cls, func: Callable[[str, List, bool], None]):
        cls.send_message_to_source = func
