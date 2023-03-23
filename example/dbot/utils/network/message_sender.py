# message_sender.py
import requests
<<<<<<<< HEAD:dzmicro/utils/network/message_sender.py
from dzmicro.utils.urlencoding_message import urlencoding_message

def send_message_to_platform(message, source_id, platform=None):
    from dzmicro.utils.network import consul_client
========
from dbot.utils.urlencoding_message import urlencoding_message

def send_message_to_platform(message, source_id, platform=None):
    from dbot.utils.network import consul_client
>>>>>>>> 5db5c8d65bf9963ee23a28ac253e0f4045b1a5f0:example/dbot/utils/network/message_sender.py
    platform_name = consul_client.download_key_value('config/platform', '""')
    if platform is None:
        platform = consul_client.discover_service(platform_name)
    ip, port = platform
    url = f'http://{ip}:{port}/api/v1/service_message'
    response = requests.post(url, json={'message': message, 'source_id': source_id})
    return response.json()

# message broker专用
def send_message_to_source(message: str, source_id):
    gid, qid = source_id
    urlencoded_message = urlencoding_message(message)
    if gid is None:
        requests.get(f'http://127.0.0.1:5700/send_private_msg?user_id={qid}&message={urlencoded_message}')
    else:   
        requests.get(f'http://127.0.0.1:5700/send_group_msg?group_id={gid}&message={urlencoded_message}')