import socket
from typing import Dict
from dzmicro.utils.judge_same_listener import judge_same_listener

def upload_service_commands() -> None:
    from dzmicro.conf import RouteInfo
    from dzmicro.app import FuncDict
    from dzmicro.utils import ConsulClient
    route_info = RouteInfo()
    func_dict = FuncDict()
    consul_client = ConsulClient()
    service_name = route_info.get_service_name()
    keyword = func_dict.get_keyword()
    commands = func_dict.get_commands()
    consul_client.update_key_value({f'{service_name}/config': {'keyword': keyword,'commands': commands}})

def request_listen(request_command, command, source_id, should_listen)-> None:
    from dzmicro.conf import RouteInfo
    from dzmicro.app import FuncDict
    from dzmicro.utils.network import ConsulClient
    route_info = RouteInfo()
    func_dict = FuncDict()
    consul_client = ConsulClient()
    service_name = route_info.get_service_name()
    # ip需要获取IPV4，配置中是0.0.0.0，不能从配置文件中读取
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    port = route_info.get_service_port()
    keyword = func_dict.get_keyword()
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
