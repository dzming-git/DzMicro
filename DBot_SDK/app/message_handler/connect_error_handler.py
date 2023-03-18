# connect_error_handler.py
from DBot_SDK.utils import send_message_to_cqhttp

def connect_error_handler(gid=None, qid=None):
    message = '连接错误'
    if gid:
        message = f'[CQ:at,qq={qid}]' + message
    send_message_to_cqhttp(message, gid, qid)