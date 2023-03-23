# keyword_error_handler.py
from dzmicro.utils import send_message_to_source

def keyword_error_handler(source_id):
    gid, qid = source_id
    message = '关键词错误'
    if gid:
        message = f'[CQ:at,qq={qid}]' + message
    send_message_to_source(message, source_id)