# consul_client.py
import consul
import socket

class ConsulClient:
    def __init__(self, host='localhost', port=8500):
        self.consul = consul.Consul(host=host, port=port)

    def register_service(self, service_name, service_port, service_tags=None):
        """
        注册服务到Consul
        """
        service_id = f'{service_name}-{socket.gethostname()}'
        service_address = socket.gethostbyname(socket.gethostname())
        service_check = consul.Check.http(url=f'http://{service_address}:{service_port}/health', interval='10s')
        self.consul.agent.service.register(name=service_name, service_id=service_id, address=service_address, port=service_port, tags=service_tags, check=service_check)
        return service_id

    def update_key_value(self, dict_to_upload: dict):
        """
        将字典上传Consul
        """
        for key, value in dict_to_upload.items():
            self.consul.kv.put(key, str(value))

    def download_key_value(self, key: str):
        """
        从Consul下载指定的Key Value
        """
        index, data = self.consul.kv.get(key)
        if data:
            return data['Value'].decode()
        else:
            return None

    def deregister_service(self, service_id):
        """
        从Consul中注销服务
        """
        self.consul.agent.service.deregister(service_id)

    def discover_services(self, service_name):
        """
        发现服务
        """
        services = self.consul.catalog.service(service_name)[1]
        return [(service['ServiceAddress'], service['ServicePort']) for service in services]

consul_client = ConsulClient()
