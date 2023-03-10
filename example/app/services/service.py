import time
from DBot_SDK import send_message

def countdown(gid=None, qid=None, msg_list=[]):
    time_countdown = int(msg_list[0])
    while time_countdown > 0:
        send_message(f'倒计时 {time_countdown}', gid, qid)
        time_countdown -= 1
        time.sleep(1)
    send_message('倒计时 结束', gid, qid)


def func2(gid=None, qid=None, msg_list=[]):
    send_message('This is func2', gid, qid)

def func3(gid=None, qid=None, msg_list=[]):
    send_message('This is func3', gid, qid)

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