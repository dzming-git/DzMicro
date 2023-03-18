# message_handler.py
import re
import threading
from DBot_SDK.app import BotCommands, keyword_error_handler, command_error_handler, permission_denied, service_offline, connect_error_handler
from DBot_SDK.utils.network import publish_task, heartbeat_manager
from DBot_SDK.utils import listener_manager
from DBot_SDK.utils.network import consul_client
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
            ip = message.get('ip')
            port = message.get('port')
            service_name = message.get('service_name')
            json = message.get('json', {})
            gid = json.get('gid')
            qid = json.get('qid')
            if heartbeat_manager.check_online(service_name) is False:
                service_offline(gid, qid)
            else:
                try:
                    authorized = publish_task(ip, port, json)
                    # None不处理，False告知权限不足
                    if authorized is False:
                        permission_denied(gid=gid, qid=qid)
                    time.sleep(0.1)
                except:
                    connect_error_handler(gid, qid)
    
    def add_message_queue(self, service_name, command, args, gid, qid, is_user_call, service=None):
        # 发送给监听者会传入service参数
        if service is None:
            service = consul_client.discover_service(service_name)
        if service:
            service_ip = service[0]
            service_port = service[1]
            message_json = {
                'ip': service_ip,
                'port': service_port,
                'service_name': service_name,
                'json': {'command': command, 'args': args, 'gid': gid, 'qid': qid, 'is_user_call': is_user_call}
            }
            self.message_queue.put(message_json)

    def message_handler(self, message: str, gid=None, qid=None):
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
        listeners = listener_manager.get_listeners()
        for listener in listeners:
            service_name = listener.get('service_name')
            port = listener.get('port')
            ip = listener.get('ip')
            command = listener.get('command')
            listen_gid = listener.get('gid')
            listen_qid = listener.get('qid')
            if gid == listen_gid:
                self.add_message_queue(service_name, command, [message], gid, qid, False, service=(ip, port))

message_handler_thread = MessageHandlerThread()
