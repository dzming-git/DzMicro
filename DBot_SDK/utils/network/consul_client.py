# consul_client.py
import consul
import socket
import time
import threading
import json
import re
import random
from typing import Dict
from DBot_SDK.utils import compare_dicts

class WatchKVThread(threading.Thread):
    def __init__(self, c):
        super().__init__(name=f'WatchKV')
        self._c = c
        self._stop = False
        self._kv = {}
    
    def stop(self):
        self._stop = True

    def on_config_changed(self, config_dict: Dict, change):
        from DBot_SDK.app import BotCommands
        if change == 'add':
            pattern = r"DBot_(\w+)/config"
            for key, value in config_dict.items():
                match = re.search(pattern, key)
                if match:
                    service_name = f'DBot_{match.group(1)}'
                    keyword = value.get('keyword')
                    BotCommands.add_keyword(keyword, service_name)
                    commands = value.get('commands')
                    if service_name and commands:
                        for command in commands:
                            BotCommands.add_commands(keyword, command)

    def on_listener_changed(self, listener_dict: Dict, change):
        from DBot_SDK.utils import listener_manager
        if change == 'add':
            pattern = r"DBot_(\w+)/listener"
            for key, value in listener_dict.items():
                match = re.search(pattern, key)
                if match:
                    service_name = f'DBot_{match.group(1)}'
                    keyword = value.get('keyword')
                    command = value.get('command')
                    ip = value.get('ip')
                    port = value.get('port')
                    gid = value.get('gid')
                    qid = value.get('qid')
                    should_listen = True
                    listener_manager.update_listeners(service_name, keyword, command, ip, port, gid, qid, should_listen)

    def on_add_kv(self, added_dict: Dict):
        print(f'添加\n{added_dict}\n')
        self.on_config_changed(added_dict, 'add')
        self.on_listener_changed(added_dict, 'add')

    def on_deleted_kv(self, deleted_dict):
        #TODO 配置文件删除
        print(f'删除\n{deleted_dict}\n')

    def on_modified_kv(self, modified_dict):
        #TODO 配置文件修改
        print(f'修改\n{modified_dict}\n')

    def run(self):
        while not self._stop:
            new_kv = {}
            while True:
                try:
                    # 获取指定文件夹下的所有key
                    keys = self._c.kv.get('DBot_', keys=True)[1]
                    break
                except:
                    print('下载字典失败，正在重试')
                    time.sleep(1)

            # 读取所有key的值，并将结果存储在字典中
            for key in keys:
                while True:
                    try:
                        data = self._c.kv.get(key)[1].get('Value', '')
                        break
                    except:
                        print('下载字典失败，正在重试')
                        time.sleep(1)
                json_data = self.decode_data(data)
                if json_data is not None:
                    new_kv[key] = json_data
            added, deleted, modified = compare_dicts(self._kv, new_kv)
            if added:
                self.on_add_kv(added)
            if deleted:
                self.on_deleted_kv(deleted)
            if modified:
                self.on_modified_kv(modified)

            self._kv = new_kv
            time.sleep(0.1)

    def decode_data(self, data):
        if data is None:
            return None
        elif type(data) is bytes:
            decoded_data = data.decode('utf-8')
        elif type(data) is str:
            decoded_data = data
        json_data = json.loads(decoded_data)
        return json_data

class ConsulClient:
    def __init__(self, host='localhost', port=8500, token=''):
        self.consul = consul.Consul(host=host, port=port)
        self.set_token(token)
        

    
    def set_token(self, token):
        if token:
            self.consul.token = token
            self._watch_kv_thread = WatchKVThread(self.consul)
            self._watch_kv_thread.start()
    
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
            while True:
                try:
                    self.consul.kv.put(key, str(value).encode('utf-8'))
                    break
                except consul.base.ConsulException:
                    print(f'上传字典{dict}失败，正在重试')
                    time.sleep(1)

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
        发现服务，返回所有设备信息
        """
        # 过滤掉不健康的服务
        services = self.consul.health.service(service_name, passing=True)[1]
        return [(service.get('Service', {}).get('Address'), service.get('Service', {}).get('Port')) for service in services]

    def discover_service(self, service_name):
        """
        发现服务，随机返回其中一个设备信息
        """
        services = self.discover_services(service_name)
        return random.choice(services)

# raise IndexError('Cannot choose from an empty sequence') from None
    def check_port_available(self, sname: str, sip: str, sport: int):
        if sip == '0.0.0.0' or sip == '127.0.0.1':
            sip = socket.gethostbyname(socket.gethostname())
        # 获取所有已注册的服务
        services = self.consul.agent.services()

        # 遍历所有已注册的服务，获取它们的 IP 和端口号
        service_instances = {}
        for service_id in services:
            service_name = services[service_id]['Service']
            _, instances = self.consul.health.service(service_name, passing=True)
            for instance in instances:
                ip = instance['Service']['Address']
                port = instance['Service']['Port']
                if service_name not in service_instances:
                    service_instances[service_name] = []
                service_instances[service_name].append((ip, port))
        
        # 逐个检查服务列表和对应的实例 IP 和端口号
        for name, instances in service_instances.items():
            for ip, port in instances:
                if sip == ip and sport == port and sname != name:
                    print(f'{ip}:{port}已被{name}占用')
                    return False
        return True

    def register_consul(self, app, name, port):
        '''
        服务开启前,注册consul
        '''
        id = self.register_service(name, port, [])
        app.config.update({'id': id})

    def deregister_service(self, app):
        '''
        服务结束后,注销consul
        '''
        id = app.config['id']
        self.deregister_service(self, id)
            
    def discover_message_broker(self, service_name):
        """
        发现机器人消息代理
        """
        services = self.discover_services(service_name)
        if services:
            from DBot_SDK.conf import RouteInfo
            message_broker = services[0]
            RouteInfo.update_message_broker(ip=message_broker[0], port=message_broker[1])
            return True
        print('消息代理未开启')
        return False

consul_client = ConsulClient()
