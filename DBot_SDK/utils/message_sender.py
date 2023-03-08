# message_sender.py
import requests

def send_result_message_to_message_broker(message, gid=None, qid=None):
    from DBot_SDK.conf.route_info import RouteInfo
    ip = RouteInfo.get_message_broker_ip()
    port = RouteInfo.get_message_broker_port()
    endport = RouteInfo.get_message_broker_endpoint('service_results')
    url = f'http://{ip}:{port}/{endport}'
    response = requests.post(url, json={'message': message, 'gid': gid, 'qid': qid})
    return response.json()