# consul_client.py
import consul
import socket
import time
import threading
import json
import re
import random
from flask import Flask
from typing import Dict, List, Union
from dzmicro.utils import compare_dicts
from dzmicro.utils.singleton import singleton


class WatchKVThread(threading.Thread):
    def __init__(self, c: consul, prefix: str) -> None:
        super().__init__(name=f'WatchKV')
        self._c = c
        self._prefix = prefix
        self._stop = False
        self._kv = {}
    
    def stop(self) -> None:
        self._stop = True

    def on_config_changed(self, config_dict: Dict[str, any], change: str) -> None:
        from dzmicro.app import BotCommands
        bot_commands = BotCommands()
        if change == 'add':
            pattern = fr"{self._prefix}(\w+)/config"
            for key, value in config_dict.items():
                match = re.search(pattern, key)
                if match:
                    service_name = f'{match.group(1)}'
                    keyword = value.get('keyword')
                    bot_commands.add_keyword(keyword, service_name)
                    commands = value.get('commands')
                    if service_name and commands:
                        for command in commands:
                            bot_commands.add_commands(keyword, command)

    def on_listener_changed(self, listener_dict: Dict[str, any], change: str) -> None:
        from dzmicro.utils import ListenerManager
        listener_manager = ListenerManager()
        pattern = fr"{self._prefix}(\w+)/listeners"
        for key, value in listener_dict.items():
            match = re.search(pattern, key)
            if match:
                if change == 'add':
                    service_name = f'{match.group(1)}'
                    #TODO 需不需要比较service_name和value中的service_name是否一致？
                    listener_manager.update_listeners(value)
                elif change == 'modify':
                    #TODO 完善listener_manager.update_listeners的功能，让他可以自动适应添加与修改
                    listener_manager.update_listeners(value.get('old'), is_rm=True)
                    listener_manager.update_listeners(value.get('new'))
                elif change == 'delete':
                    listener_manager.update_listeners(value, is_rm=True)


    def on_add_kv(self, added_dict: Dict[str, any]) -> None:
        print(f'添加\n{added_dict}\n')
        self.on_config_changed(added_dict, 'add')
        self.on_listener_changed(added_dict, 'add')

    def on_deleted_kv(self, deleted_dict: Dict[str, any]) -> None:
        #TODO 配置文件删除
        print(f'删除\n{deleted_dict}\n')
        self.on_config_changed(deleted_dict, 'delete')
        self.on_listener_changed(deleted_dict, 'delete')

    def on_modified_kv(self, modified_dict: Dict[str, any]) -> None:
        #TODO 配置文件修改
        print(f'修改\n{modified_dict}\n')
        self.on_config_changed(modified_dict, 'modify')
        self.on_listener_changed(modified_dict, 'modify')

    def run(self) -> None:
        consul_client = ConsulClient()
        while not self._stop:
            new_kv = {}
            while True:
                try:
                    # 获取指定文件夹下的所有key
                    #TODO 这个前缀也可以在kv中配置
                    keys = consul_client.download_key_value(self._prefix, [], True)
                    break
                except:
                    print('下载字典失败，正在重试')
                    time.sleep(1)

            # 读取所有key的值，并将结果存储在字典中
            for key in keys:
                while True:
                    try:
                        json_data = consul_client.download_key_value(key, '')
                        new_kv[key] = json_data
                        break
                    except:
                        print('下载字典失败，正在重试')
                        time.sleep(1)
            added, deleted, modified = compare_dicts(self._kv, new_kv)
            if added:
                self.on_add_kv(added)
            if deleted:
                self.on_deleted_kv(deleted)
            if modified:
                self.on_modified_kv(modified)

            self._kv = new_kv
            time.sleep(1)

@singleton
class ConsulClient:
    def __init__(self, host: str = 'localhost', port: int = 8500, prefix: str = '', token: str = '') -> None:
        self.consul = consul.Consul(host=host, port=port)
        self.set_prefix(prefix)
        self.set_token(token)
    
    def set_prefix(self, prefix: str = '') -> None:
        self._prefix = prefix
    
    def set_token(self, token: str) -> None:
        if token:
            self.consul.token = token

    def start_watch_kv(self) -> None:
        self._watch_kv_thread = WatchKVThread(self.consul, self._prefix)
        self._watch_kv_thread.start()
    
    def register_service(self, service_name: str, service_port: Union[str, int], service_tags: List[str] = []) -> str:
        """
        注册服务到Consul
        """
        service_id = f'{service_name}-{socket.gethostname()}'
        service_address = socket.gethostbyname(socket.gethostname())
        service_check = consul.Check.http(url=f'http://{service_address}:{service_port}/health', interval='10s')
        self.consul.agent.service.register(name=service_name, service_id=service_id, address=service_address, port=service_port, tags=service_tags, check=service_check)
        return service_id

    def update_key_value(self, dict_to_upload: Dict[str, any]) -> None:
        """
        将字典上传Consul
        """
        for key, value in dict_to_upload.items():
            while True:
                try:
                    value_json = json.dumps(value)
                    self.consul.kv.put(key, value_json.encode('utf-8'))
                    break
                except consul.base.ConsulException:
                    print(f'上传字典{dict}失败，正在重试')
                    time.sleep(1)

    def download_key_value(self, key: str, default: any = None, keys: bool = False) -> any:
        """
        从Consul下载指定的Key Value
        """
        index, data = self.consul.kv.get(key, keys=keys)
        if data:
            if keys:
                return data
            else:
                value_json = data['Value'].decode('utf-8')
                value = json.loads(value_json)
                return value
        else:
            return default

    def deregister_service(self, service_id: str) -> None:
        """
        从Consul中注销服务
        """
        self.consul.agent.service.deregister(service_id)

    def discover_services(self, service_name: str) -> List[List[str]]:
        """
        发现服务，返回所有设备信息
        """
        #TODO 考虑添加查询表缓存，需要考虑查询表的刷新；刷新时机可以选择为WatchKVThread发现变动时
        # 过滤掉不健康的服务
        try:
            services = self.consul.health.service(service_name, passing=True)[1]
            return [[service.get('Service', {}).get('Address', ''), service.get('Service', {}).get('Port', '')] for service in services]
        except:
            return [[]]

    def discover_service(self, service_name: str) -> Union[List[List[str]], None]:
        """
        发现服务，随机返回其中一个设备信息
        """
        services = self.discover_services(service_name)
        if not services:
            return None
        return random.choice(services)

    def check_port_available(self, sname: str, sip: str, sport: Union[int, str]) -> bool:
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

    def register_consul(self, app: Flask, name: str, port: Union[str, int], tags: List[str]) -> None:
        '''
        服务开启前,注册consul
        '''
        id = self.register_service(name, port, tags)
        app.config.update({'id': id})

    def deregister_service(self, app: Flask) -> None:
        '''
        服务结束后,注销consul
        '''
        id = app.config['id']
        self.deregister_service(self, id)
