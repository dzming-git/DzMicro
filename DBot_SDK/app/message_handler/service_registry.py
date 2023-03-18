import threading
from DBot_SDK.utils import consul_client
from datetime import datetime

class ServiceRegistry:
    '''
    _services = {
        'DBot_example': {
            'ip':
            'port':
            'last_update_time':
        }
    }
    '''
    _services = {}
    '''
    _listens = [
        {
            'service_name':
            'command':
            'gid':
            'qid':
        }
    ]

    '''
    _listens = []

    @classmethod
    def add_service(cls, service_name, ip, port):
        cls._services[service_name] = {
            'ip': ip,
            'port': port,
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
    def update_listens(cls, service_name, command, gid, qid, should_listen):
        #TODO 删除监听还没写
        if should_listen:
            should_add = True
            for listen in cls._listens:
                if \
                    service_name == listen.get('service_name') and \
                    command == listen.get('command') and \
                    gid == listen.get('gid'):
                    if (gid is None and qid == listen.get('qid')) or gid:
                        should_add = False
            if should_add:
                cls._listens.append({
                    'service_name': service_name,
                    'command': command,
                    'gid': gid,
                    'qid': qid
                })
            else:
                pass
    
    @classmethod
    def get_listens(cls):
        '''
        获取目前监听状态的服务和申请监听的指令
        '''
        return cls._listens

    @classmethod
    def update_services(cls):
        # do something to update services

        # call this method again after a delay of 60 seconds
        threading.Timer(60, cls.update_services).start()
