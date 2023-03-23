# service_offline_handler.py
from DBot_SDK.utils import send_message_to_source

def service_offline(source_id):
    gid, qid = source_id
    message = '处理该关键词的服务处于离线状态，请联系管理员。'
    if gid:
        message = f'[CQ:at,qq={qid}]' + message
    send_message_to_source(message, gid, qid)
