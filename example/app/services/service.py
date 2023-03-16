import time
from DBot_SDK import send_message, Authority

def help(gid=None, qid=None, args=[]):
    permission_level = Authority.get_permission_level(gid, qid)
    permission = Authority.get_permission_by_level(permission_level)
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

def auto_echo(gid=None, qid=None, args=[]):
    if not args or args[0] == '开始':
        from DBot_SDK.conf import RouteInfo
        import requests
        message_broker_ip = RouteInfo.get_message_broker_ip()
        message_broker_port = RouteInfo.get_message_broker_port()
        endpoint = RouteInfo.get_message_broker_endpoint('service_listen')
        service_name = RouteInfo.get_service_name()
        #TODO 考虑要不要将keyword设置为全局变量，这里似乎可以为其他服务程序开启监听
        keyword = KEYWORD
        command = '复读'
        requests.post(f'http://{message_broker_ip}:{message_broker_port}/{endpoint}', 
                    json={'service_name': service_name, 
                            'keyword': keyword,
                            'command': command,
                            'gid': gid,
                            'qid': qid,
                            'should_listen': True})
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
    '自动复读': {
        'func': auto_echo,
        'permission': 'ADMIN'
        },
    '复读': {
        'func': echo,
        'permission': 'INTERNAL'
        },
    }