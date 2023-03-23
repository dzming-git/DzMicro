# permission_denied_handler.py
from dzmicro.utils import send_message_to_source

def permission_denied(source_id):
    gid, qid = source_id
    message = '权限不足'
    if gid:
        message = f'[CQ:at,qq={qid}]' + message
    send_message_to_source(message, source_id)
