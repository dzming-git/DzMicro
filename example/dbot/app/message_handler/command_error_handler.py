# command_error_handler.py
<<<<<<<< HEAD:dzmicro/app/message_handler/command_error_handler.py
from dzmicro.utils import send_message_to_source
========
from dbot.utils import send_message_to_source
>>>>>>>> 5db5c8d65bf9963ee23a28ac253e0f4045b1a5f0:example/dbot/app/message_handler/command_error_handler.py

def command_error_handler(source_id):
    gid, qid = source_id
    message = '命令错误'
    if gid:
        message = f'[CQ:at,qq={qid}]' + message
    send_message_to_source(message, source_id)