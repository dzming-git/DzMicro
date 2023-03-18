import requests
import json

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

def publish_task(ip, port, json):
    print(f'{ip} {port} {json}')
    url = f'http://{ip}:{port}/api/v1/receive_command'
    response = requests.post(url, json=json).json()
    authorized = response.get('permission', None)
    return authorized
