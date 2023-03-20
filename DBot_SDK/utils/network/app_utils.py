import requests
import json
import socket
from DBot_SDK.utils.judge_same_listener import judge_same_listener

def upload_service_commands():
    # 注册支持的指令到消息代理程序
    from DBot_SDK.conf import RouteInfo
    from DBot_SDK.app import FuncDict
    service_name = RouteInfo.get_service_name()
    keyword = FuncDict.get_keyword()
    commands = FuncDict.get_commands()
    k = f'{service_name}/config'
    v = json.dumps({
        'keyword': keyword,
        'commands': commands
    })
    from DBot_SDK.utils import consul_client
    consul_client.update_key_value({k: v})

def request_listen(request_command, command, gid, qid, should_listen):
    from DBot_SDK.conf import RouteInfo
    from DBot_SDK.app import FuncDict
    from DBot_SDK.utils.network import consul_client
    import json
    service_name = RouteInfo.get_service_name()
    # ip需要获取IPV4，配置中是0.0.0.0，不能从配置文件中读取
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    port = RouteInfo.get_service_port()
    keyword = FuncDict.get_keyword()
    k = f'{service_name}/listeners'
    json_str = consul_client.download_key_value(k)
    if json_str is None:
        consul_listeners = []
    else:
        consul_listeners = json.loads(json_str)  # List[Dict]
        consul_listeners = [] if consul_listeners is None else consul_listeners
    # 删除同一个监听配置，再添加新的配置
    for i, consul_listener in enumerate(consul_listeners):
        if judge_same_listener(listener=consul_listener,
                            service_name=service_name,
                            keyword=keyword,
                            command=command,
                            gid=gid,
                            qid=qid):
            consul_listeners.pop(i)
            break
    consul_listeners.append({
        'service_name': service_name, 
        'keyword': keyword,
        'request_command': request_command,
        'command': command,
        'ip': ip, 
        'port': port,
        'gid': gid,
        'qid': qid,
        'should_listen': should_listen})
    v = json.dumps(consul_listeners)
    consul_client.update_key_value({k: v})


def publish_task(ip, port, json):
    print(f'{ip} {port} {json}')
    url = f'http://{ip}:{port}/api/v1/receive_command'
    response = requests.post(url, json=json).json()
    authorized = response.get('permission', None)
    return authorized
