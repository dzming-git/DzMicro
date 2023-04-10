from dzmicro.utils.network import MQThread
from typing import Dict, Tuple
import threading
from pika.spec import BasicProperties

def task_handler(uuid: str, task: Dict[str, any], props: BasicProperties) -> Tuple[bool, Dict[str, any], BasicProperties]:
    from dzmicro.utils import singleton_server_manager
    server_unique_info = singleton_server_manager.get_server_unique_info(uuid)
    result_dict = {}
    command = task.get('command', '')
    source_id = task.get('source_id', [])
    is_user_call = task.get('is_user_call', True)
    permission = True
    if is_user_call:
        authority = server_unique_info.authority
        permission = authority.check_command_permission(command=command, source_id=source_id)
    if permission:
        def exe_task(task: Dict[str, any]) -> None:
            func_dict = server_unique_info.func_dict
            func = func_dict.get_func(command)
            func(uuid, task)

        single_task_thread = threading.Thread(target=exe_task, args=(task, ), name=f'ExeTask:{command}')
        single_task_thread.start()
    result_dict['permission'] = permission
    result_dict['source_id'] = source_id
    props_send = BasicProperties()
    props_send.correlation_id = props.correlation_id
    return True, result_dict, props_send

def service_message_reply(uuid: str, task: Dict[str, any], props: BasicProperties) -> Tuple[bool, Dict[str, any], BasicProperties]:
    from dzmicro.utils import singleton_server_manager
    server_unique_info = singleton_server_manager.get_server_unique_info(uuid)
    mq_reply = server_unique_info.mq_replay_thread
    mq_reply.ack_reply(props.correlation_id, task)
    return True, {}, None

def set_consumer(mq_consumer_thread: MQThread):
    mq_consumer_thread.declare_queue('receive_command')
    mq_consumer_thread.set_consumer(queue_name='receive_command', task_handler=task_handler, reply=True)
    mq_consumer_thread.set_consumer(queue_name='service_message_reply', task_handler=service_message_reply, reply=False)
