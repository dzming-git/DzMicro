# app.py
from flask import Flask
import time
import threading
from werkzeug.serving import make_server
from DBot_SDK.api import route_registration, message_broker_route_registration
from DBot_SDK.utils import consul_client
from DBot_SDK.conf import ConfigFromUser
from DBot_SDK.utils.network import heartbeat_manager, upload_service_commands

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

        # 设置心跳管理器身份，并启动
        heartbeat_manager.set_identity(is_message_broker=ConfigFromUser.is_message_broker())
        heartbeat_manager.start()
        
        if ConfigFromUser.is_message_broker():
            message_broker_route_registration(self._app)
        else:
            success_connect = False
            while True:
                success_connect = consul_client.discover_message_broker(RouteInfo.get_message_broker_name())
                if success_connect:
                    break
                print('连接DBot平台程序失败，正在重连')
                time.sleep(1)
            upload_service_commands()
            route_registration(self._app)

        consul_client.register_consul(self._app, self.server_name, port)
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
        consul_client.deregister_service(self._app)

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