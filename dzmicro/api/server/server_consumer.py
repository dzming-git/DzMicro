from dzmicro.utils.network import MQThread
from typing import Dict, Tuple
import threading
from pika.spec import BasicProperties

def task_handler(task: Dict[str, any], props: BasicProperties) -> Tuple[bool, Dict[str, any], BasicProperties]:
    result_dict = {}
    command = task.get('command', '')
    source_id = task.get('source_id', [])
    is_user_call = task.get('is_user_call', True)
    permission = True
    if is_user_call:
        from dzmicro.conf import Authority
        authority = Authority()
        permission = authority.check_command_permission(command=command, source_id=source_id)
    if permission:
        def exe_task(task: Dict[str, any]) -> None:
            from dzmicro.app import FuncDict
            func_dict = FuncDict()
            func = func_dict.get_func(command)
            func(task)

        single_task_thread = threading.Thread(target=exe_task, args=(task, ), name=f'ExeTask:{command}')
        single_task_thread.start()
    result_dict['permission'] = permission
    result_dict['source_id'] = source_id
    props_send = BasicProperties()
    props_send.correlation_id = props.correlation_id
    return True, result_dict, props_send

def service_message_reply(task: Dict[str, any], props: BasicProperties) -> Tuple[bool, Dict[str, any], BasicProperties]:
    from dzmicro.utils.network.mq import MQReplyThread
    mq_reply = MQReplyThread()
    mq_reply.ack_reply(props.correlation_id, task)
    return True, {}, None

def start_consume() -> MQThread:
    from dzmicro.utils.network.mq import create_mq
    mq_thread = create_mq()
    mq_thread.declare_queue('receive_command')
    mq_thread.set_consumer(queue_name='receive_command', task_handler=task_handler, reply=True)
    mq_thread.set_consumer(queue_name='service_message_reply', task_handler=service_message_reply, reply=False)
    mq_thread.start()
    return mq_thread
