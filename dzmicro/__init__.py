from dzmicro.conf import DzMicro
from dzmicro.utils import WatchDogThread
from dzmicro.utils.network import request_listen
from dzmicro.conf import Authority

from dzmicro.utils import singleton_server_manager
from typing import List
def send_message(uuid: str,  message: str, source_id: List[any]):
    server_unique_info = singleton_server_manager.get_server_unique_info(uuid)
    server_unique_info.message_sender.send_message_to_platform(message.strip(), source_id)


__all__ = ['DzMicro', 'WatchDogThread', 'send_message', 'request_listen', 'Authority']