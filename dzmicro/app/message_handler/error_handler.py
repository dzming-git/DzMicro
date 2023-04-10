from typing import List


def command_error_handler(uuid: str, source_id: List[any]) -> None:
    message = '命令错误'
    from dzmicro.utils import singleton_server_manager
    message_sender = singleton_server_manager.servers[uuid].message_sender
    message_sender.send_message_to_source(message, source_id, True)

def connect_error_handler(uuid: str, source_id: List[any]) -> None:
    message = '连接错误'
    from dzmicro.utils import singleton_server_manager
    message_sender = singleton_server_manager.servers[uuid].message_sender
    message_sender.send_message_to_source(message, source_id, True)

def keyword_error_handler(uuid: str, source_id: List[any]) -> None:
    message = '关键词错误'
    from dzmicro.utils import singleton_server_manager
    message_sender = singleton_server_manager.servers[uuid].message_sender
    message_sender.send_message_to_source(message, source_id, True)

def permission_denied(uuid: str, source_id: List[any]) -> None:
    message = '权限不足'
    from dzmicro.utils import singleton_server_manager
    message_sender = singleton_server_manager.servers[uuid].message_sender
    message_sender.send_message_to_source(message, source_id, True)

def service_offline(uuid: str, source_id: List[any]) -> None:
    message = '处理该关键词的服务处于离线状态，请联系管理员。'
    from dzmicro.utils import singleton_server_manager
    message_sender = singleton_server_manager.servers[uuid].message_sender
    message_sender.send_message_to_source(message, source_id, True)