# message_handler.py
import re
import requests
import threading
from DBot_SDK.app import BotCommands, keyword_error_handler, command_error_handler, permission_denied
from DBot_SDK.utils.message_sender import send_message_to_cqhttp
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
        if keyword:
            if keyword not in keywords:
                keyword_error_handler(gid, qid)
            else:
                commands = BotCommands.get_commands(keyword)
                if command not in commands:
                    command_error_handler(gid, qid)
                service_name = BotCommands.get_service_name(keyword)
                sends.append((service_name, command, args))
        # 监听消息转发
        #TODO 正常的指令是否需要处理？
        listens = ServiceRegistry.get_listens()
        for listen in listens:
            service_name = listen.get('service_name')
            command = listen.get('command')
            listen_gid = listen.get('gid')
            listen_qid = listen.get('qid')
            #TODO 可能存在问题，感觉for循环应该就只有一个或0个，实现的不优雅
            if gid == listen_gid:
                if sends:
                    service_name_in_sends, command_in_sends, args_in_sends = sends[0]
                    if service_name != service_name_in_sends or command != command_in_sends:
                        sends.append((service_name, command, [message]))
                else:
                    sends.append((service_name, command, [message]))
        for service_name, command, args in sends:
            service_info = ServiceRegistry.get_service(service_name)
            if service_info is not None:
                service_ip = service_info['ip']
                service_port = service_info['port']
                endpoint = service_info['endpoints']['receive_command']
                url = f"http://{service_ip}:{service_port}/{endpoint}"
                message_json = {
                    'url':url,
                    'json': {'command': command, 'args': args, 'gid': gid, 'qid': qid}
                }
                self.message_queue.put(message_json)

message_handler_thread = MessageHandlerThread()
