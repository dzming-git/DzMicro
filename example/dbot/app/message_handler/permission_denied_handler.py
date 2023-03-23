# permission_denied_handler.py
<<<<<<<< HEAD:dzmicro/app/message_handler/permission_denied_handler.py
from dzmicro.utils import send_message_to_source
========
from dbot.utils import send_message_to_source
>>>>>>>> 5db5c8d65bf9963ee23a28ac253e0f4045b1a5f0:example/dbot/app/message_handler/permission_denied_handler.py

def permission_denied(source_id):
    gid, qid = source_id
    message = '权限不足'
    if gid:
        message = f'[CQ:at,qq={qid}]' + message
    send_message_to_source(message, source_id)
