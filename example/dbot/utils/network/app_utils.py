import requests
import json
import socket
from typing import Dict
<<<<<<<< HEAD:dzmicro/utils/network/app_utils.py
from dzmicro.utils.judge_same_listener import judge_same_listener

def upload_service_commands():
    from dzmicro.conf import RouteInfo
    from dzmicro.app import FuncDict
    service_name = RouteInfo.get_service_name()
    keyword = FuncDict.get_keyword()
    commands = FuncDict.get_commands()
    from dzmicro.utils import consul_client
    consul_client.update_key_value({f'{service_name}/config': {'keyword': keyword,'commands': commands}})

def request_listen(request_command, command, source_id, should_listen):
    from dzmicro.conf import RouteInfo
    from dzmicro.app import FuncDict
    from dzmicro.utils.network import consul_client
========
from dbot.utils.judge_same_listener import judge_same_listener

def upload_service_commands():
    from dbot.conf import RouteInfo
    from dbot.app import FuncDict
    service_name = RouteInfo.get_service_name()
    keyword = FuncDict.get_keyword()
    commands = FuncDict.get_commands()
    from dbot.utils import consul_client
    consul_client.update_key_value({f'{service_name}/config': {'keyword': keyword,'commands': commands}})

def request_listen(request_command, command, source_id, should_listen):
    from dbot.conf import RouteInfo
    from dbot.app import FuncDict
    from dbot.utils.network import consul_client
>>>>>>>> 5db5c8d65bf9963ee23a28ac253e0f4045b1a5f0:example/dbot/utils/network/app_utils.py
    service_name = RouteInfo.get_service_name()
    # ip需要获取IPV4，配置中是0.0.0.0，不能从配置文件中读取
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    port = RouteInfo.get_service_port()
    keyword = FuncDict.get_keyword()
    consul_listeners = consul_client.download_key_value(f'{service_name}/listeners')
    consul_listeners = [] if consul_listeners is None else consul_listeners
    # 删除同一个监听配置，再添加新的配置
    for i, consul_listener in enumerate(consul_listeners):
        listener1 = {
                'service_name': service_name,
                'keyword': keyword,
                'command': command,
                'source_id': source_id
            }
        if judge_same_listener(consul_listener, listener1):
            consul_listeners.pop(i)
            break
    if should_listen:
        consul_listeners.append({
            'service_name': service_name, 
            'keyword': keyword,
            'request_command': request_command,
            'command': command,
            'ip': ip, 
            'port': port,
            'source_id': source_id})
    consul_client.update_key_value({f'{service_name}/listeners': consul_listeners})


def publish_task(message: Dict):
    print(f'publish_task\n{message}\n')
    service_address = message.get('service_address', (None, None))
    service_ip, service_port = service_address
    send_json = message.get('send_json', {})
    url = f'http://{service_ip}:{service_port}/api/v1/receive_command'
    response = requests.post(url, json=send_json).json()
    authorized = response.get('permission', None)
    return authorized
