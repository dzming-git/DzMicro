# command_error_handler.py
from DBot_SDK.utils.message_sender import Msg_struct, send_message_to_cqhttp

def command_error_handler(gid=None, qid=None):
    message = '命令错误'
    if gid:
        message = f'[CQ:at,qq={qid}]' + message
    msg_struct = Msg_struct(gid=gid, qid=qid, msg=message)
    send_message_to_cqhttp(msg_struct)