from dzmicro.utils.network import MQThread
from typing import Dict, Tuple
import threading

def task_handler(task: Dict[str, any]) -> Tuple[bool, Dict[str, any]]:
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
    return True, result_dict

def start_consume() -> MQThread:
    from dzmicro.utils.network.mq import create_mq
    mq_thread = create_mq()
    mq_thread.declare_queue('receive_command')
    mq_thread.set_consumer(queue_name='receive_command', task_handler=task_handler, reply=True)
    mq_thread.start()
    return mq_thread
