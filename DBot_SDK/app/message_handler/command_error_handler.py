# command_error_handler.py
from DBot_SDK.utils.message_sender import send_message_to_cqhttp

def command_error_handler(gid=None, qid=None):
    message = '命令错误'
    if gid:
        message = f'[CQ:at,qq={qid}]' + message
    send_message_to_cqhttp(message, gid, qid)