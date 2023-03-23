import time
import socket
from DBot_SDK import send_message, Authority, request_listen

def help(task):
    source_id = task.get('source_id', None)
    platform = task.get('platform', None)
    gid, qid = source_id
    permission_level = Authority.get_permission_level(source_id)
    permission = Authority.get_permission_by_level(permission_level)
    if gid:
        message = f'[CQ:at,qq={qid}]\n'
    message = f'关键词 {KEYWORD}\n当前权限 {permission}\n可调用指令如下\n'
    for command in list(func_dict.keys()):
        if Authority.check_command_permission(command, source_id):
            message += f'  - {command}\n'
    send_message(message.strip(), source_id, platform)

def countdown(task):
    source_id = task.get('source_id', None)
    args = task.get('args', [])
    platform = task.get('platform', None)
    if not args:
        send_message('缺少参数', source_id, platform)
    else:
        time_countdown = int(args[0])
        while time_countdown > 0:
            send_message(f'倒计时 {time_countdown}', source_id, platform)
            time_countdown -= 1
            time.sleep(1)
        send_message('倒计时 结束', source_id, platform)

def get_ip(task):
    source_id = task.get('source_id', None)
    platform = task.get('platform', None)
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    send_message(ip_address, source_id, platform)

def auto_echo(task):
    source_id = task.get('source_id', None)
    args = task.get('args', [])
    platform = task.get('platform', None)
    request_command = '自动复读'
    command = '复读'
    if not args or args[0] == '开始':        
        request_listen(request_command, command, source_id, True)
        send_message('自动复读开始', source_id, platform)
    elif args[0] == '停止':
        request_listen(request_command, command, source_id, False)
        send_message('自动复读停止', source_id, platform)

def echo(task):
    source_id = task.get('source_id', None)
    args = task.get('args', [])
    platform = task.get('platform', None)
    if args:
        send_message(args[0], source_id, platform)

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