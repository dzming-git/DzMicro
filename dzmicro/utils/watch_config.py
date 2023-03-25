# watch_config.py
import time
import os
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from typing import Callable

class ConfigFileHandler(FileSystemEventHandler):
    def __init__(self, config_path: str, reload_func: Callable[[], None]):
        self.config_path = config_path
        self.reload_func = reload_func
        self.last_modified_time = os.path.getmtime(self.config_path)

    def on_modified(self, event: FileModifiedEvent) -> None:
        if not event.is_directory and os.path.normpath(self.config_path) == os.path.normpath(event.src_path):
            current_time = time.time()
            time_interval = current_time - self.last_modified_time
            self.last_modified_time = current_time
            # VSCode编辑文本时会连续保存多次
            if time_interval < 0.5:
                return
            else:
                self.reload_func()
                print(f'配置文件{self.config_path}被修改，重新加载')

class WatchDogThread(threading.Thread):
    def __init__(self, config_path: str, reload_func: Callable[[], None]) -> None:
        self.config_path = config_path
        self.reload_func = reload_func
        self._stop = False
        config_name = os.path.basename(config_path)
        super().__init__(name=f'WatchDog_{config_name}')
    
    def run(self) -> None:
        event_handler = ConfigFileHandler(self.config_path, self.reload_func)
        observer = Observer()
        observer.schedule(event_handler, '.', recursive=True)
        observer.start()
        while not self._stop:
            time.sleep(1)
        observer.stop()
        observer.join()
    
    def stop(self) -> None:
        self._stop = True
