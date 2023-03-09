import time
from DBot_SDK import send_message

def countdown(gid=None, qid=None, msg_list=[]):
    time_countdown = int(msg_list[0])
    while time_countdown > 0:
        send_message(f'倒计时 {time_countdown}', gid, qid)
        time_countdown -= 1
        time.sleep(1)
    message_parts = []
    message_parts.append('倒计时 结束')
    message_send = '\n'.join(message_parts).rstrip('\n')
    return message_send

def func2(gid=None, qid=None, msg_list=[]):
    message_parts = []
    message_parts.append('This is func2')
    message_send = '\n'.join(message_parts).rstrip('\n')
    return message_send

def func3(gid=None, qid=None, msg_list=[]):
    message_parts = []
    message_parts.append('This is func3')
    message_send = '\n'.join(message_parts).rstrip('\n')
    return message_send

def add(gid=None, qid=None, msg_list=[]):
    message_parts = []
    try:
        int_list = list(map(int, msg_list))
        sum_of_ints = sum(int_list)
        message_str = ''
        for num in int_list:
            message_str += f'{num} + '
        message_str = message_str[0:-2] + f'= {sum_of_ints}'
        message_parts.append(message_str)
    except:
        message_parts.append('input error')
    message_send = '\n'.join(message_parts).rstrip('\n')
    return message_send

func_dict = {
    '#倒计时': {
        'func': countdown,
        'permission': 'USER'
        },
    '#CMD2': {
        'func': func2,
        'permission': 'ADMIN'
        },
    '#CMD3': {
        'func': func3,
        'permission': 'MASTER'
        },
    }