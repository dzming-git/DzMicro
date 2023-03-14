# service.py
import time
from DBot_SDK import ConfigFromUser, server_thread
from app.services.service import func_dict

def load_conf():
    ConfigFromUser.Authority_load_config('conf/authority/authority.yaml')
    ConfigFromUser.RouteInfo_load_config('conf/route_info/route_info.yaml')

if __name__ == '__main__': 
    load_conf()
    ConfigFromUser.set_keyword('#测试')
    ConfigFromUser.set_func_dict(func_dict)
    server_thread.set_safe_start(True)
    if server_thread.start():
        while True:
            time.sleep(10)
