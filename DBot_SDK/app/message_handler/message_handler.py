# message_handler.py
import re
import threading
from DBot_SDK.app import BotCommands, keyword_error_handler, command_error_handler, permission_denied, service_offline, connect_error_handler
from DBot_SDK.utils.network import publish_task, heartbeat_manager, consul_client
from DBot_SDK.utils import listener_manager, judge_same_listener
from DBot_SDK.conf import RouteInfo
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
            gid = send_json.get('gid')
            qid = send_json.get('qid')
            if heartbeat_manager.check_online(service_name) is False:
                service_offline(gid, qid)
            else:
                try:
                    authorized = publish_task(message)
                    # None不处理，False告知权限不足
                    if authorized is False:
                        permission_denied(gid=gid, qid=qid)
                    time.sleep(0.1)
                except:
                    connect_error_handler(gid, qid)
    
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
        
        listeners = listener_manager.get_listeners()
        keywords = list(BotCommands.get_keywords())
        keyword, command, args = message_split(message)

        include_keyword = False
        correct_keyword = False
        
        # args0表示指令相应， args表示监听的转发
        arg0 = None
        args = []
        #TODO 含有关键词的不按照监听的方式转发，未来可能有监听指令的功能，待完善
        if keyword:
            include_keyword = True
            if keyword not in keywords:
                keyword_error_handler(gid, qid)
            else:
                correct_keyword = True
                commands = BotCommands.get_commands(keyword)
                if command not in commands:
                    command_error_handler(gid, qid)
                service_name = BotCommands.get_service_name(keyword)
                is_user_call = True
                service_address = consul_client.discover_service(service_name)
                if service_address is not None:
                    service_info = {'service_name': service_name, 'service_address': service_address}
                    send_json = {'command': command, 'args': args, 'gid': gid, 'qid': qid, 'is_user_call': is_user_call}
                    arg0 = (service_info, send_json)
                else:
                    connect_error_handler(gid, qid)

        # 监听消息转发
        for listener in listeners:
            listener_service_name = listener.get('service_name')
            listener_port = listener.get('port')
            listener_ip = listener.get('ip')
            listener_command = listener.get('command')
            listener_gid = listener.get('gid')
            listener_qid = listener.get('qid')
            is_user_call = False
            service_address = listener_ip, listener_port
            if include_keyword and correct_keyword:
                if judge_same_listener(listener=listener,
                                       service_name=service_name,
                                       keyword=keyword,
                                       command=listener.get('command'),  # 凑条件通过判断
                                       gid=gid,
                                       qid=qid):
                    if command == listener.get('request_command'):  # 接收到的指令与申请监听的指令是同一个指令
                        service_info, send_json = arg0
                        service_info['service_address'] = (listener_ip, listener_port)  # 转发给处理监听的服务
                        arg0 = (service_info, send_json)
            else:
                service_info = {'service_name': listener_service_name, 'service_address': service_address}
                send_json = {'command': listener_command, 'args': [message], 'gid': gid, 'qid': qid, 'is_user_call': is_user_call}
                if gid is None and qid == listener_qid:  # 私聊
                    args.append(service_info, send_json)
                elif gid == listener_gid:  # 群聊
                    args.append(service_info, send_json)
        if arg0:
            self.add_message_queue(*arg0)
        for arg in args:
            self.add_message_queue(*arg)

message_handler_thread = MessageHandlerThread()
