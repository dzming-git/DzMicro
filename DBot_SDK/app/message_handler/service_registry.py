import threading
from DBot_SDK.utils.service_discovery.consul_client import consul_client
from datetime import datetime

class serviceRegistry:
    _services = {}

    @classmethod
    def add_service(cls, service_name, ip, port):
        cls._services[service_name] = {
            'ip': ip,
            'port': port,
            'endpoints': {},
            'last_update_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        print(f"Registered service {service_name} at {ip}:{port}")

    @classmethod
    def remove_service(cls, service_name):
        cls._services.pop(service_name, None)
        print(f"Removed service {service_name}")

    @classmethod
    def add_service_from_consul(cls, service_name):
        services = consul_client.discover_services(service_name)
        if services:
            service_ip = services[0][0]
            service_port = services[0][1]
            cls.add_service(service_name, service_ip, service_port)
            return True
        return False

    @classmethod
    def get_service(cls, service_name):
        service_info = cls._services.get(service_name)
        if service_info is None:
            if cls.add_service_from_consul(service_name):
                service_info = cls._services.get(service_name)
        return service_info
    
    @classmethod
    def add_service_endpoint(cls, service_name, usage, endpoint):
        if service_name in list(cls._services.keys()):
            cls._services[service_name]['endpoints'][usage] = endpoint
        else:
            if cls.add_service_from_consul(service_name):
                cls._services[service_name]['endpoints'][usage] = endpoint

    @classmethod
    def get_service_endpoint(cls, service_name, usage):
        try:
            return cls._services[service_name]['endpoints'][usage]
        except KeyError:
            return None

    @classmethod
    def update_services(cls):
        # do something to update services

        # call this method again after a delay of 60 seconds
        threading.Timer(60, cls.update_services).start()
