# service_offline_handler.py
from dzmicro.utils import send_message_to_source

def service_offline(source_id):
    message = '处理该关键词的服务处于离线状态，请联系管理员。'

    send_message_to_source(message, source_id)
