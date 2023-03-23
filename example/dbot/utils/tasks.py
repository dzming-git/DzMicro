# task.py
import threading
from queue import Queue
<<<<<<<< HEAD:dzmicro/utils/tasks.py
from dzmicro.app import FuncDict
========
from dbot.app import FuncDict
>>>>>>>> 5db5c8d65bf9963ee23a28ac253e0f4045b1a5f0:example/dbot/utils/tasks.py

class TaskThread(threading.Thread):
    def __init__(self):
        super().__init__(name='TaskThread')
        self._task_queue = Queue()
        self._stop = False
        super().start()

    def add_task(self, command, args, source_id):
        self._task_queue.put({
            'command': command,
            'args': args,
            'source_id': source_id
        })
    
    def exe_task(self, task):
        command = task['command']
        func = FuncDict.get_func(command)
        func(task)

    def run(self):
        while not self._stop:
            task = self._task_queue.get(block=True)
            command = task['command']
            single_task_thread = threading.Thread(target=self.exe_task, args=(task, ), name=f'ExeTask:{command}')
            single_task_thread.start()
            
    
    def stop(self):
        self._stop = False

task_thread = TaskThread()
