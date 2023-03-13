# message_sender.py
import requests

def send_message_to_message_broker(message, gid=None, qid=None):
    from DBot_SDK.conf.route_info import RouteInfo
    ip = RouteInfo.get_message_broker_ip()
    port = RouteInfo.get_message_broker_port()
    endport = RouteInfo.get_message_broker_endpoint('service_message')
    url = f'http://{ip}:{port}/{endport}'
    response = requests.post(url, json={'message': message, 'gid': gid, 'qid': qid})
    return response.json()

# message broker专用
class Msg_struct:
    def __init__(self, gid=None, qid=None, msg=''):
        self.gid = gid
        self.qid = qid
        self.msg = msg

# message broker专用
def send_message_to_cqhttp(msg_struct: Msg_struct):
    if msg_struct.gid is None:
        requests.get(f'http://127.0.0.1:5700/send_private_msg?user_id={msg_struct.qid}&message={msg_struct.msg}')
    else:   
        requests.get(f'http://127.0.0.1:5700/send_group_msg?group_id={msg_struct.gid}&message={msg_struct.msg}')