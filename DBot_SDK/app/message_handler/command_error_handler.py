# command_error_handler.py
from DBot_SDK.utils import send_message_to_source

def command_error_handler(source_id):
    gid, qid = source_id
    message = '命令错误'
    if gid:
        message = f'[CQ:at,qq={qid}]' + message
    send_message_to_source(message, source_id)