import time
import socket
from DBot_SDK import send_message, Authority, request_listen

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
    request_command = '自动复读'
    command = '复读'
    if not args or args[0] == '开始':        
        request_listen(request_command, command, gid, qid, True)
        send_message('自动复读开始', gid, qid)
    elif args[0] == '停止':
        request_listen(request_command, command, gid, qid, False)
        send_message('自动复读停止', gid, qid)

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