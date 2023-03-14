# message_handler.py
import re
import requests
import threading
from DBot_SDK.app.message_handler.bot_commands import BotCommands
from DBot_SDK.app.message_handler.keyword_error_handler import keyword_error_handler
from DBot_SDK.app.message_handler.permission_denied_handler import permission_denied
from DBot_SDK.utils.message_sender import send_message_to_cqhttp
from DBot_SDK.app.message_handler.service_registry import serviceRegistry
from queue import Queue
import time

class MessageHandlerThread(threading.Thread):
    def __init__(self):
        super().__init__(name='MessageHandlerThread')
        self.stop = False
        self.message_queue = Queue()
        super().start()
    
    def run(self):
        while not self.stop:
            message = self.message_queue.get(block=True)
            url = message['url']
            json = message['json']
            try:
                response = requests.post(url, json=json)
                result_dict = response.json()
                permission = result_dict['permission']
                gid = json['gid']
                qid = json['qid']
                if not permission:
                    permission_denied(gid=gid, qid=qid)
                print(f"Message forwarded to {url}")
                time.sleep(0.1)
            except:
                send_message_to_cqhttp('连接错误', gid, qid)    
    
    def message_handler(self, message: str, gid=None, qid=None):
        # TODO:需要同步修改
        def message_split(message):
            pattern = r'(#\w+)\s*(.*)'
            match = re.match(pattern, message.strip())
            if match:
                keyword = match.group(1)
                param_list = match.group(2).strip().split()
                if param_list:
                    command = param_list[0]
                    param_list = param_list[1:]
                else:
                    command = 'default'
                return keyword, command, param_list
            else:
                return None, None, None
        keywords = list(BotCommands.get_keywords())
        keyword, command, param_list = message_split(message)
        if keyword:
            if keyword not in keywords:
                keyword_error_handler(gid, qid)
            else:
                service_name = BotCommands.get_service_name(keyword)
                service_info = serviceRegistry.get_service(service_name)
                if service_info is not None:
                    service_ip = service_info['ip']
                    service_port = service_info['port']
                    endpoint = service_info['endpoints']['receive_command']
                    url = f"http://{service_ip}:{service_port}/{endpoint}"
                    message = {
                        'url':url,
                        'json': {'command': command, 'args': param_list, 'gid': gid, 'qid': qid}
                    }
                    self.message_queue.put(message)

message_handler_thread = MessageHandlerThread()
