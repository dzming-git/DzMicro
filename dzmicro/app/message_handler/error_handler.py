from dzmicro.utils import send_message_to_source

def command_error_handler(source_id):
    message = '命令错误'
    send_message_to_source(message, source_id, True)

def connect_error_handler(source_id):
    message = '连接错误'
    send_message_to_source(message, source_id, True)

def keyword_error_handler(source_id):
    message = '关键词错误'
    send_message_to_source(message, source_id, True)

def permission_denied(source_id):
    message = '权限不足'
    send_message_to_source(message, source_id, True)

def service_offline(source_id):
    message = '处理该关键词的服务处于离线状态，请联系管理员。'
    send_message_to_source(message, source_id, True)