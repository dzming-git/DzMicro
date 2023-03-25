from dzmicro.utils import MessageSender
from typing import List

message_sender = MessageSender()

def command_error_handler(source_id: List[any]) -> None:
    message = '命令错误'
    message_sender.send_message_to_source(message, source_id, True)

def connect_error_handler(source_id: List[any]) -> None:
    message = '连接错误'
    message_sender.send_message_to_source(message, source_id, True)

def keyword_error_handler(source_id: List[any]) -> None:
    message = '关键词错误'
    message_sender.send_message_to_source(message, source_id, True)

def permission_denied(source_id: List[any]) -> None:
    message = '权限不足'
    message_sender.send_message_to_source(message, source_id, True)

def service_offline(source_id: List[any]) -> None:
    message = '处理该关键词的服务处于离线状态，请联系管理员。'
    message_sender.send_message_to_source(message, source_id, True)