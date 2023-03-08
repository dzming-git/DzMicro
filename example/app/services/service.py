def func1(gid=None, qid=None, msg_list=[]):
    message_parts = []
    message_parts.append('This is func1')
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
    '#CMD1': {
        'func': lambda gid=None, qid=None, msg_list=[]: func1(gid, qid, msg_list),
        'permission_level': 1
    },
    '#CMD2': {
        'func': lambda gid=None, qid=None, msg_list=[]: func2(gid, qid, msg_list),
        'permission_level': 2
    },
    '#CMD3': {
        'func': lambda gid=None, qid=None, msg_list=[]: func3(gid, qid, msg_list),
        'permission_level': 3
    },
    }