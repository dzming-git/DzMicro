# service.py
import time
from app import func_dict, KEYWORD

from DBot_SDK import ConfigFromUser
ConfigFromUser.Authority_load_config('conf/authority/authority.yaml')
ConfigFromUser.RouteInfo_load_config('conf/route_info/route_info.yaml')
ConfigFromUser.ConsulInfo_load_config('conf/consul_info/consul_info.yaml')
ConfigFromUser.set_keyword(KEYWORD)
ConfigFromUser.set_func_dict(func_dict)

from DBot_SDK import server_thread

if __name__ == '__main__': 
    server_thread.set_safe_start(True)
    if server_thread.start():
        while True:
            time.sleep(10)
