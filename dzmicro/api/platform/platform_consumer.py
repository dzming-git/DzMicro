from dzmicro.utils.network import MQThread
from typing import Dict, Tuple
from dzmicro.app.message_handler.error_handler import permission_denied
from pika.spec import BasicProperties

# 将服务程序传回的信息转发回信息源
def send_to_source(uuid: str, task: Dict[str, any], props: BasicProperties) -> Tuple[bool, Dict[str, any], BasicProperties]:
    from dzmicro.utils import singleton_server_manager
    server_unique_info = singleton_server_manager.get_server_unique_info(uuid)
    message = task.get('message')
    source_id = task.get('source_id')
    message_sender = server_unique_info.message_sender
    message_sender.send_message_to_source(message, source_id)
    props_send = BasicProperties()
    props_send.correlation_id = props.correlation_id
    return True, {}, props_send

# 接收发布任务的权限返回情况
def receive_command_reply(uuid: str, task: Dict[str, any], props: BasicProperties) -> Tuple[bool, Dict[str, any], BasicProperties]:
    from dzmicro.utils import singleton_server_manager
    server_unique_info = singleton_server_manager.get_server_unique_info(uuid)
    mq_reply = server_unique_info.mq_replay_thread
    mq_reply.ack_reply(props.correlation_id, task)
    return True, {}, None

def set_consumer(mq_consumer_thread: MQThread):
    mq_consumer_thread.declare_queue('service_message')
    mq_consumer_thread.set_consumer(queue_name='service_message', task_handler=send_to_source, reply=True)
    mq_consumer_thread.set_consumer(queue_name='receive_command_reply', task_handler=receive_command_reply, reply=False)

