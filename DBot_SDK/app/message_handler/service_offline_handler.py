# service_offline_handler.py
from DBot_SDK.utils import send_message_to_cqhttp

def service_offline(gid=None, qid=None):
    message = '处理该关键词的服务处于离线状态，请联系管理员。'
    if gid:
        message = f'[CQ:at,qq={qid}]' + message
    send_message_to_cqhttp(message, gid, qid)
