from dzmicro.utils.network import MQThread
from typing import Dict, Tuple
from dzmicro.app.message_handler.error_handler import permission_denied

# 将服务程序传回的信息转发回信息源
def send_to_source(task: Dict[str, any]) -> Tuple[bool, Dict[str, any]]:
    message = task.get('message')
    source_id = task.get('source_id')
    from dzmicro.utils import MessageSender
    message_sender = MessageSender()
    message_sender.send_message_to_source(message, source_id)
    return True, {'OK': True}

# 接收发布任务的权限返回情况
def receive_premission(task: Dict[str, any]) -> Tuple[bool, Dict[str, any]]:
    permission = task.get('permission', None)
    source_id = task.get('source_id', [])
    if permission is False:
        permission_denied(source_id)
    return True, {'OK': True}

def start_consume() -> MQThread:
    from dzmicro.utils.network.mq import create_mq
    mq_thread = create_mq()
    mq_thread.declare_queue('service_message')
    mq_thread.set_consumer(queue_name='service_message', task_handler=send_to_source, reply=False)
    mq_thread.set_consumer(queue_name='receive_command_reply', task_handler=receive_premission, reply=False)
    mq_thread.start()
    return mq_thread
