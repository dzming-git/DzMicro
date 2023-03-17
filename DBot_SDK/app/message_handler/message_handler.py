# message_handler.py
import re
import requests
import threading
from DBot_SDK.app import BotCommands, keyword_error_handler, command_error_handler, permission_denied
from DBot_SDK.utils import send_message_to_cqhttp
from DBot_SDK.app import ServiceRegistry
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
            gid = json['gid']
            qid = json['qid']
            try:
                response = requests.post(url, json=json)
                result_dict = response.json()
                permission = result_dict['permission']
                # None不处理，False告知权限不足
                if permission is False:
                    permission_denied(gid=gid, qid=qid)
                print(f"Message forwarded to {url}")
                time.sleep(0.1)
            except:
                send_message_to_cqhttp('连接错误', gid, qid)
    
    def add_message_queue(self, service_name, command, args, gid, qid, is_user_call):
        service_info = ServiceRegistry.get_service(service_name)
        if service_info is not None:
            service_ip = service_info['ip']
            service_port = service_info['port']
            endpoint = service_info['endpoints']['receive_command']
            url = f"http://{service_ip}:{service_port}/{endpoint}"
            message_json = {
                'url':url,
                'json': {'command': command, 'args': args, 'gid': gid, 'qid': qid, 'is_user_call': is_user_call}
            }
            self.message_queue.put(message_json)

    def message_handler(self, message: str, gid=None, qid=None):
        sends = []
        def message_split(message):
            pattern = r'(#\w+)\s*(.*)'
            match = re.match(pattern, message.strip())
            if match:
                keyword = match.group(1)
                args = match.group(2).strip().split()
                if args:
                    command = args[0]
                    args = args[1:]
                else:
                    command = '帮助'
                return keyword, command, args
            else:
                return None, None, None
        keywords = list(BotCommands.get_keywords())
        keyword, command, args = message_split(message)
        #TODO 含有关键词的不按照监听的方式转发，未来可能有监听指令的功能，待完善
        if keyword:
            if keyword not in keywords:
                keyword_error_handler(gid, qid)
            else:
                commands = BotCommands.get_commands(keyword)
                if command not in commands:
                    command_error_handler(gid, qid)
                service_name = BotCommands.get_service_name(keyword)
                self.add_message_queue(service_name, command, args, gid, qid, True)
                return
        # 监听消息转发
        listens = ServiceRegistry.get_listens()
        for listen in listens:
            service_name = listen.get('service_name')
            command = listen.get('command')
            listen_gid = listen.get('gid')
            listen_qid = listen.get('qid')
            if gid == listen_gid:
                self.add_message_queue(service_name, command, [message], gid, qid, False)

message_handler_thread = MessageHandlerThread()
