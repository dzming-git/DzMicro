# app.py
from flask import Flask
import threading
import json
from werkzeug.serving import make_server
from dbot.api import route_registration, platform_route_registration
from dbot.utils import consul_client
from dbot.conf import DBot
from dbot.utils.network import heartbeat_manager, upload_service_commands

class ServerThread(threading.Thread):
    def init(self):
        self.safe_start = False
        self._server = None
        from dbot.conf import RouteInfo
        self.server_name = RouteInfo.get_service_name()
        ip = RouteInfo.get_service_ip()
        port = RouteInfo.get_service_port()
        tags = RouteInfo.get_service_tags()
            
        if self.safe_start:
            is_available = consul_client.check_port_available(self.server_name, ip, port)
            if not is_available:
                return False
        super().__init__(name=f'ServerThread_{self.server_name}')
        self._app = Flask(__name__)

        # 设置心跳管理器身份，并启动
        heartbeat_manager.set_identity(is_platform=DBot.is_platform())
        heartbeat_manager.start()

        upload_service_commands()
        
        if DBot.is_platform():
            platform_route_registration(self._app)
            # 在consul的kv中配置本服务为平台服务
            consul_client.update_key_value({f'config/platform': self.server_name})
        else:
            route_registration(self._app)

        consul_client.register_consul(self._app, self.server_name, port, tags)
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