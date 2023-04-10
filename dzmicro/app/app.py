# app.py
from flask import Flask
import threading
from werkzeug.serving import make_server
from dzmicro.utils.network import upload_service_commands

class ServerThread(threading.Thread):
    def __init__(self, uuid: str, is_platform: bool = False) -> None:
        super().__init__()
        self.uuid = uuid
        self.is_platform = is_platform
        self.safe_start = False

    def set_server_unique_info(self) -> None:
        from dzmicro.utils import singleton_server_manager
        self.server_unique_info = singleton_server_manager.get_server_unique_info(self.uuid)

    def init(self) -> bool: 
        self._server = None
        server_name = self.server_unique_info.route_info.get_service_name()
        ip = self.server_unique_info.route_info.get_service_ip()
        port = self.server_unique_info.route_info.get_service_port()
        tags = self.server_unique_info.route_info.get_service_tags()
        if self.safe_start:
            is_available = self.server_unique_info.consul_client.check_port_available(server_name, ip, port)
            if not is_available:
                return False
        self.setName(f'ServerThread_{server_name}')
        self._app = Flask(__name__)

        upload_service_commands(self.uuid)
        
        if self.is_platform:
            from dzmicro.api.platform.platform_routes import route_registration
            # 在consul的kv中配置本服务为平台服务
            self.server_unique_info.consul_client.update_key_value({f'config/platform': server_name})
        else:
            from dzmicro.api.server.server_routes import route_registration
        route_registration(self._app)

        self.server_unique_info.consul_client.register_consul(self._app, server_name, port, tags)
        self._server = make_server(host=ip, port=port, app=self._app)
        return True

    def set_safe_start(self, flag: bool) -> None:
        '''
        设置安全开始，则会检查配置中的ip与port是否已经被占用
        但会有较大的启动时间开销
        '''
        self.safe_start = flag

    def start(self) -> bool:
        if self.init():
            super().start()
            return True
        return False
        
    def destory_app(self) -> None:
        self.server_unique_info.consul_client.deregister_service(self._app)

    def run(self) -> None:
        server_name = self.server_unique_info.route_info.get_service_name()
        print(f'{server_name}已运行')
        self._server.serve_forever()
        print(f'{server_name}已结束')
    
    def stop(self) -> None:
        self._server.shutdown()
    
    def restart(self) -> bool:
        server_name = self.server_unique_info.route_info.get_service_name()
        print(f'{server_name}正在重启')
        return False
        # TODO 待重构
        # if self._server:
        #     self.stop()
        # return self.start()
