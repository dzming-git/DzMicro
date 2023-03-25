from dzmicro.conf import DzMicro
from dzmicro.utils import WatchDogThread
from dzmicro.utils.network import request_listen
from dzmicro.conf import Authority

from dzmicro.utils.network import MessageSender
message_sender = MessageSender()
send_message = message_sender.send_message_to_platform

__all__ = ['DzMicro', 'WatchDogThread', 'send_message', 'request_listen', 'Authority']