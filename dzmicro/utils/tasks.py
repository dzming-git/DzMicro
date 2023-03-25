# task.py
import threading
from queue import Queue
from typing import List, Dict
from dzmicro.utils.singleton import singleton

@singleton
class TaskThread(threading.Thread):
    def __init__(self) -> None:
        super().__init__(name='TaskThread')
        self._task_queue = Queue()
        self._stop = False
        super().start()

    def add_task(self, command: str, args: List[str], source_id: List[any]) -> None:
        self._task_queue.put({
            'command': command,
            'args': args,
            'source_id': source_id
        })
    
    def exe_task(self, task: Dict[str, any]) -> None:
        from dzmicro.app import FuncDict
        func_dict = FuncDict()
        command = task['command']
        func = func_dict.get_func(command)
        func(task)

    def run(self) -> None:
        while not self._stop:
            task = self._task_queue.get(block=True)
            command = task['command']
            single_task_thread = threading.Thread(target=self.exe_task, args=(task, ), name=f'ExeTask:{command}')
            single_task_thread.start()
            
    
    def stop(self) -> None:
        self._stop = False
