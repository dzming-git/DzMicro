# app.py
from flask import Flask
import requests
import time
import json
import threading
from werkzeug.serving import make_server
from DBot_SDK.api import route_registration, message_broker_route_registration
from DBot_SDK.utils.service_discovery import register_consul, discover_message_broker, deregister_service, message_broker_endpoints_upload
from DBot_SDK.utils.service_discovery import consul_client
from DBot_SDK.conf import ConfigFromUser


def download_message_broker_endpoints():
    # 下载消息代理的endpoint
    from DBot_SDK.conf import RouteInfo
    message_broker_consul_key = RouteInfo.get_message_broker_consul_key('message_broker_endpoints')
    message_broker_endpoints_info_str = consul_client.download_key_value(message_broker_consul_key)
    dictionary = json.loads(message_broker_endpoints_info_str.replace("'", "\""))
    if dictionary:
        for endpoint, usage in dictionary.items():
            RouteInfo.add_message_broker_endpoint(usage=usage, endpoint=endpoint)
        return True
    return False

def upload_service_commands():
    # 注册支持的指令到消息代理程序
    from DBot_SDK.conf import RouteInfo
    from DBot_SDK.app import FuncDict
    message_broker_ip = RouteInfo.get_message_broker_ip()
    message_broker_port = RouteInfo.get_message_broker_port()
    endpoint = RouteInfo.get_message_broker_endpoint('service_commands')
    service_name = RouteInfo.get_service_name()
    keyword = FuncDict.get_keyword()
    commands = FuncDict.get_commands()
    requests.post(f'http://{message_broker_ip}:{message_broker_port}/{endpoint}', 
                  json={
        'service_name': service_name, 
        'keyword': keyword,
        'commands': commands})
    
def upload_service_endpoints():
    # 注册支持的endpoint到消息代理程序
    from DBot_SDK.conf import RouteInfo
    message_broker_ip = RouteInfo.get_message_broker_ip()
    message_broker_port = RouteInfo.get_message_broker_port()
    endpoint = RouteInfo.get_message_broker_endpoint('service_endpoints')
    service_name = RouteInfo.get_service_name()
    endpoints_info = RouteInfo.get_service_endpoints_info()
    requests.post(f'http://{message_broker_ip}:{message_broker_port}/{endpoint}', json={'service_name': service_name, 'endpoints_info': endpoints_info})

class ServerThread(threading.Thread):
    def init(self):
        self.safe_start = False
        self._server = None
        from DBot_SDK.conf import RouteInfo
        if ConfigFromUser.is_message_broker():
            self.server_name = RouteInfo.get_message_broker_name()
            ip = RouteInfo.get_message_broker_ip()
            port = RouteInfo.get_message_broker_port()
        else:
            self.server_name = RouteInfo.get_service_name()
            ip = RouteInfo.get_service_ip()
            port = RouteInfo.get_service_port()
            
        if self.safe_start:
            is_available = consul_client.check_port_available(self.server_name, ip, port)
            if not is_available:
                return False
        super().__init__(name=f'ServerThread_{self.server_name}')
        self._app = Flask(__name__)

        if ConfigFromUser.is_message_broker():
            message_broker_route_registration(self._app)
            message_broker_endpoints_upload()
        else:
            success_connect = False
            while True:
                success_connect = \
                    discover_message_broker(RouteInfo.get_message_broker_name()) and \
                    download_message_broker_endpoints()
                if success_connect:
                    break
                print('连接DBot平台程序失败，正在重连')
                time.sleep(1)
            upload_service_commands()
            upload_service_endpoints()
            route_registration(self._app)

        register_consul(self._app, self.server_name, port)
        self._server = make_server(host=ip, port=port, app=self._app)
        return True

    def set_safe_start(self, flag):
        '''
        设置安全开始，则会检查配置中的ip与port是否已经被占用
        但会有较大的启动时间开销
        '''
        self.safe_start = flag

    def start(self):
        if self.init():
            super().start()
            return True
        return False
        
    def destory_app(self):
        deregister_service(self._app)

    def run(self):
        print(f'{self.server_name}已运行')
        self._server.serve_forever()
        print(f'{self.server_name}已结束')
    
    def stop(self):
        self._server.shutdown()
    
    def restart(self):
        print(f'{self.server_name}正在重启')
        if self._server:
            self.stop()
        return self.start()

server_thread = ServerThread()