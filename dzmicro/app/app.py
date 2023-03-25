# app.py
from flask import Flask
import threading
from werkzeug.serving import make_server
from dzmicro.api import route_registration, platform_route_registration
from dzmicro.utils import ConsulClient
from dzmicro.utils.network import HeartbeatManager, upload_service_commands
from dzmicro.utils.singleton import singleton

@singleton
class ServerThread(threading.Thread):
    def init(self, is_platform: bool = False) -> bool:
        self.safe_start = False
        self._server = None
        self._consul_client = ConsulClient()
        from dzmicro.conf import RouteInfo
        route_info = RouteInfo()
        self.server_name = route_info.get_service_name()
        ip = route_info.get_service_ip()
        port = route_info.get_service_port()
        tags = route_info.get_service_tags()
            
        if self.safe_start:
            is_available = self._consul_client.check_port_available(self.server_name, ip, port)
            if not is_available:
                return False
        super().__init__(name=f'ServerThread_{self.server_name}')
        self._app = Flask(__name__)

        # 设置心跳管理器身份，并启动
        heartbeat_manager = HeartbeatManager()
        heartbeat_manager.set_identity(is_platform=is_platform)
        heartbeat_manager.start()

        upload_service_commands()
        
        if is_platform:
            platform_route_registration(self._app)
            # 在consul的kv中配置本服务为平台服务
            self._consul_client.update_key_value({f'config/platform': self.server_name})
        else:
            route_registration(self._app)

        self._consul_client.register_consul(self._app, self.server_name, port, tags)
        self._server = make_server(host=ip, port=port, app=self._app)
        return True

    def set_safe_start(self, flag: bool) -> None:
        '''
        设置安全开始，则会检查配置中的ip与port是否已经被占用
        但会有较大的启动时间开销
        '''
        self.safe_start = flag

    def start(self, is_platform: bool = False) -> bool:
        if self.init(is_platform):
            super().start()
            return True
        return False
        
    def destory_app(self) -> None:
        self._consul_client.deregister_service(self._app)

    def run(self) -> None:
        print(f'{self.server_name}已运行')
        self._server.serve_forever()
        print(f'{self.server_name}已结束')
    
    def stop(self) -> None:
        self._server.shutdown()
    
    def restart(self) -> bool:
        print(f'{self.server_name}正在重启')
        if self._server:
            self.stop()
        return self.start()
