# connect_error_handler.py
from dbot.utils import send_message_to_source

def connect_error_handler(source_id):
    gid, qid = source_id
    message = '连接错误'
    if gid:
        message = f'[CQ:at,qq={qid}]' + message
    send_message_to_source(message, source_id)