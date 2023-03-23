# message_handler.py
import re
import threading
<<<<<<<< HEAD:dzmicro/app/message_handler/message_handler.py
from dzmicro.app import BotCommands, keyword_error_handler, command_error_handler, permission_denied, service_offline, connect_error_handler
from dzmicro.utils.network import publish_task, heartbeat_manager, consul_client
from dzmicro.utils import listener_manager, judge_same_listener
from dzmicro.conf import RouteInfo
========
from dbot.app import BotCommands, keyword_error_handler, command_error_handler, permission_denied, service_offline, connect_error_handler
from dbot.utils.network import publish_task, heartbeat_manager, consul_client
from dbot.utils import listener_manager, judge_same_listener
from dbot.conf import RouteInfo
>>>>>>>> 5db5c8d65bf9963ee23a28ac253e0f4045b1a5f0:example/dbot/app/message_handler/message_handler.py
from queue import Queue
import time
import socket

class MessageHandlerThread(threading.Thread):
    def __init__(self):
        super().__init__(name='MessageHandlerThread')
        self.stop = False
        self.message_queue = Queue()
        super().start()
    
    def run(self):
        while not self.stop:
            message = self.message_queue.get(block=True)
            service_name = message.get('service_name')
            send_json = message.get('send_json', {})
            source_id = send_json.get('source_id')
            if heartbeat_manager.check_online(service_name) is False:
                service_offline(source_id)
            else:
                try:
                    authorized = publish_task(message)
                    # None不处理，False告知权限不足
                    if authorized is False:
                        permission_denied(source_id)
                    time.sleep(0.1)
                except:
                    connect_error_handler(source_id)
    
    def add_message_queue(self, service_info, send_json):
        if service_info:
            platform_ip = socket.gethostbyname(socket.gethostname())
            platform_port = RouteInfo.get_service_port()
            message_json = {
                **service_info,
                'platform_address': (platform_ip, platform_port) if platform_ip and platform_port else None,
                'send_json': send_json
            }
            self.message_queue.put(message_json)

    def message_handler(self, message: str, source_id):
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
        
        listeners = listener_manager.get_listeners()
        keywords = list(BotCommands.get_keywords())
        keyword, command, args = message_split(message)

        include_keyword = False
        correct_keyword = False
        
        # args0表示指令相应， args_listener表示监听的转发
        arg0 = None
        args_listener = []
        #TODO 含有关键词的不按照监听的方式转发，未来可能有监听指令的功能，待完善
        if keyword:
            include_keyword = True
            if keyword not in keywords:
                keyword_error_handler(source_id)
            else:
                correct_keyword = True
                commands = BotCommands.get_commands(keyword)
                if command not in commands:
                    command_error_handler(source_id)
                service_name = BotCommands.get_service_name(keyword)
                is_user_call = True
                service_address = consul_client.discover_service(service_name)
                if service_address is not None:
                    service_info = {'service_name': service_name, 'service_address': service_address}
                    send_json = {'command': command, 'args': args, 'source_id': source_id, 'is_user_call': is_user_call}
                    arg0 = (service_info, send_json)
                else:
                    connect_error_handler(source_id)

        # 监听消息转发
        for listener in listeners:
            listener_service_name = listener.get('service_name')
            listener_port = listener.get('port')
            listener_ip = listener.get('ip')
            listener_command = listener.get('command')
            listener_source_id = listener.get('source_id')
            is_user_call = False
            service_address = listener_ip, listener_port
            if include_keyword and correct_keyword:
                listener1 = {
                    'service_name': service_name,
                    'keyword': keyword,
                    'command': listener.get('command'),  # 凑条件通过判断
                    'source_id': source_id
                }
                if judge_same_listener(listener, listener1):
                    if command == listener.get('request_command'):  # 接收到的指令与申请监听的指令是同一个指令
                        service_info, send_json = arg0
                        service_info['service_address'] = (listener_ip, listener_port)  # 转发给处理监听的服务
                        arg0 = (service_info, send_json)
            else:
                service_info = {'service_name': listener_service_name, 'service_address': service_address}
                send_json = {'command': listener_command, 'args': [message], 'source_id': source_id, 'is_user_call': is_user_call}
                if source_id == listener_source_id:
                    args_listener.append((service_info, send_json))
        if arg0:
            self.add_message_queue(*arg0)
        for arg in args_listener:
            self.add_message_queue(*arg)

message_handler_thread = MessageHandlerThread()
