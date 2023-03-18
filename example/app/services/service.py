import time
import socket
from DBot_SDK import send_message, Authority

def help(gid=None, qid=None, args=[]):
    permission_level = Authority.get_permission_level(gid, qid)
    permission = Authority.get_permission_by_level(permission_level)
    if gid:
        message = f'[CQ:at,qq={qid}]\n'
    message = f'关键词 {KEYWORD}\n当前权限 {permission}\n可调用指令如下\n'
    for command in list(func_dict.keys()):
        if Authority.check_command_permission(command, gid, qid):
            message += f'  - {command}\n'
    send_message(message.strip(), gid, qid)

def countdown(gid=None, qid=None, args=[]):
    if not args:
        send_message('缺少参数', gid, qid)
    else:
        time_countdown = int(args[0])
        while time_countdown > 0:
            send_message(f'倒计时 {time_countdown}', gid, qid)
            time_countdown -= 1
            time.sleep(1)
        send_message('倒计时 结束', gid, qid)

def get_ip(gid=None, qid=None, args=[]):
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    send_message(ip_address, gid, qid)

def auto_echo(gid=None, qid=None, args=[]):
    #TODO 这段功能需要放在SDK中
    if not args or args[0] == '开始':
        from DBot_SDK.conf import RouteInfo
        from DBot_SDK.utils.network import consul_client
        import requests
        import json
        message_broker_ip = RouteInfo.get_message_broker_ip()
        message_broker_port = RouteInfo.get_message_broker_port()
        service_name = RouteInfo.get_service_name()
        # ip需要获取IPV4，配置中是0.0.0.0，不能从配置文件中读取
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        port = RouteInfo.get_service_port()
        #TODO 这里似乎可以为其他服务程序开启监听
        keyword = KEYWORD
        command = '复读'
        k = f'{service_name}/listener'
        v = json.dumps({
            'service_name': service_name, 
            'keyword': keyword,
            'command': command,
            'ip': ip,
            'port': port,
            'gid': gid,
            'qid': qid,
            'should_listen': True})
        consul_client.update_key_value({k: v})
    send_message('自动复读开始', gid, qid)

def echo(gid=None, qid=None, args=[]):
    if args:
        send_message(args[0], gid, qid)

KEYWORD = '#测试'
func_dict = {
    '帮助':{
        'func': help,
        'permission': 'USER'
        },
    '倒计时': {
        'func': countdown,
        'permission': 'USER'
        },
    'IP':{
        'func': get_ip,
        'permission': 'USER'
        },
    '自动复读': {
        'func': auto_echo,
        'permission': 'ADMIN'
        },
    '复读': {
        'func': echo,
        'permission': 'INTERNAL'
        },
    }