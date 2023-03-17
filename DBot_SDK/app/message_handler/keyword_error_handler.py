# keyword_error_handler.py
from DBot_SDK.utils import send_message_to_cqhttp

def keyword_error_handler(gid=None, qid=None):
    message = '关键词错误'
    if gid:
        message = f'[CQ:at,qq={qid}]' + message
    send_message_to_cqhttp(message, gid, qid)