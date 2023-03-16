# message_sender.py
import requests
import urllib

def send_message_to_message_broker(message, gid=None, qid=None):
    from DBot_SDK.conf.route_info import RouteInfo
    ip = RouteInfo.get_message_broker_ip()
    port = RouteInfo.get_message_broker_port()
    endport = RouteInfo.get_message_broker_endpoint('service_message')
    url = f'http://{ip}:{port}/{endport}'
    response = requests.post(url, json={'message': message, 'gid': gid, 'qid': qid})
    return response.json()

# message broker专用
def send_message_to_cqhttp(message: str, gid=None, qid=None):
    urlencoded_message = urllib.parse.quote(message)
    if gid is None:
        requests.get(f'http://127.0.0.1:5700/send_private_msg?user_id={qid}&message={urlencoded_message}')
    else:   
        requests.get(f'http://127.0.0.1:5700/send_group_msg?group_id={gid}&message={urlencoded_message}')