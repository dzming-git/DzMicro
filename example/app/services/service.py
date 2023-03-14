import time
from DBot_SDK import send_message

def help(gid=None, qid=None, args=[]):
    message = '该关键词支持指令有：\n'
    for command in list(func_dict.keys()):
        message += f'{command}\n'
    send_message(message.strip('\n'), gid, qid)

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
    #TODO 开启监听的服务函数和接收消息的执行服务函数应该设置为不同的函数
    #TODO 接收监听指令的服务函数应该加一个不可被主动调用的标记
    if args[0] == '开始':
        from DBot_SDK.conf import RouteInfo
        import requests
        message_broker_ip = RouteInfo.get_message_broker_ip()
        message_broker_port = RouteInfo.get_message_broker_port()
        endpoint = RouteInfo.get_message_broker_endpoint('service_listen')
        service_name = RouteInfo.get_service_name()
        keyword = '#测试'
        command = '自动复读'
        requests.post(f'http://{message_broker_ip}:{message_broker_port}/{endpoint}', 
                    json={'service_name': service_name, 
                            'keyword': keyword,
                            'command': command,
                            'gid': gid,
                            'qid': qid,
                            'should_listen': True})

    send_message(args[0], gid, qid)

def func3(gid=None, qid=None, args=[]):
    send_message('This is func3', gid, qid)

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
    'CMD3': {
        'func': func3,
        'permission': 'MASTER'
        },
    }