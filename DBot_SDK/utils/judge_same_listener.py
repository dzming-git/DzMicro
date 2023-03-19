from typing import Dict

def judge_same_listener(listener: Dict, service_name, keyword, command, gid, qid):
    # 相同服务名、相同关键词、同样指令、同人私聊或同群群聊，则判定为同一个监听者
    if \
        service_name == listener.get('service_name') and \
        keyword == listener.get('keyword') and \
        command == listener.get('command') and \
        gid == listener.get('gid'):
        if \
            (gid is None and qid == listener.get('qid')) or \
            gid == listener.get('gid'):
            return True
    return False
