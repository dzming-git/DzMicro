# service.py
import time
from app import func_dict, KEYWORD
from dbot import DBot

if __name__ == '__main__': 
    dbot = DBot()
    dbot.set_authority_config('conf/authority/authority.yaml')
    dbot.set_routeInfo_config('conf/route_info/route_info.yaml')
    dbot.set_consulInfo_config('conf/consul_info/consul_info.yaml')
    dbot.set_keyword(KEYWORD)
    dbot.set_func_dict(func_dict)
    if dbot.start_server():
        while True:
            time.sleep(10)
