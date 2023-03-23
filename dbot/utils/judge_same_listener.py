from typing import Dict

def judge_same_listener(listener0: Dict, listener1: Dict):
    #TODO 原来的标准：相同服务名、相同关键词、同样指令、同人私聊或同群群聊，则判定为同一个监听者
    # 修改source_id之后的标准，同样的消息源才被判定为同一个
    compare_keys = ['service_name', 'keyword', 'command', 'source_id']
    for compaer_key in compare_keys:
          if listener0.get(compaer_key) != listener1.get(compaer_key):
                return False
    return True
