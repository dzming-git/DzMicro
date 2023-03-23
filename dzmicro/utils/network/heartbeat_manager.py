import time
import requests
import threading

class HeartbeatManager(threading.Thread):
    def __init__(self, interval=5):
        super().__init__(name='HeartbeatManagerThread')
        self._interval = interval
        self._services = {}
        self._timer = time.time()
        self._is_platform = None
    
    def set_identity(self, is_platform=False):
        self._is_platform = is_platform

    def register(self, service_name):
        if service_name not in self._services:
            print(f'服务程序 {service_name} 已上线')
        self._services[service_name] = time.time()
    
    def check_online(self, service_name):
        return service_name in self._services
    
    def heartbeat(self):
        # 定义心跳间隔时间，发送心跳的时间间隔比检测时间间隔少一点
        heartbeat_interval = self._interval * 0.9
        from dzmicro.conf.route_info import RouteInfo
        from dzmicro.utils.network import consul_client
        
        while True:
            platform_name = consul_client.download_key_value('config/platform', '""')
            platforms = consul_client.discover_services(platform_name)
            for platform in platforms:
                ip, port = platform
                service_name = RouteInfo.get_service_name()
                if ip and port and service_name:
                    url = f'http://{ip}:{port}/api/v1/heartbeat/{service_name}'
                try:
                    # 向服务发送心跳请求
                    response = requests.get(url)

                    # 检查响应的状态码
                    if response.status_code != 200:
                        print('心跳请求失败：', response.status_code)
                except:
                    print('心跳请求失败')

            time.sleep(heartbeat_interval)

    def check(self):
        now = time.time()
        try:
            for service_name, last_time in self._services.items():
                if (now - last_time) > self._interval:
                    # 将该服务程序标记为离线
                    print(f'服务程序 {service_name} 已下线')
                    del self._services[service_name]
        except RuntimeError:
            #TODO 测试时，for service_name, last_time in self._services.items()报错：RuntimeError: dictionary changed size during iteration
            pass

    def run(self):
        while self._is_platform is None:
            time.sleep(1)
        if self._is_platform:
            while True:
                if (time.time() - self._timer) > self._interval:
                    self.check()
                    self._timer = time.time()
                time.sleep(1)
        else:
            self.heartbeat()

heartbeat_manager = HeartbeatManager()
