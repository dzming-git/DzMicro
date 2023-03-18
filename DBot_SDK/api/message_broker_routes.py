# message_broker_routes.py
from flask import request, jsonify
from DBot_SDK.utils.network import heartbeat_manager

def message_broker_route_registration(app):
    @app.route('/', methods=['POST'])
    def handle_message():
        '''
        将信息源的信息转发至服务程序
        '''
        from DBot_SDK.app.message_handler.message_handler import message_handler_thread
        # 获取消息体
        message = request.json
        print(message)
        # 获取消息类型
        message_type = message.get('message_type')
        # 获取发送者id
        sender_id = message.get('sender', {}).get('user_id')
        # 获取群id
        group_id = message.get('group_id')
        # 获取原始消息内容
        raw_message = message.get('raw_message')
        # 处理私聊消息
        if message_type == 'private':
            message_handler_thread.message_handler(raw_message, qid=sender_id)
        # 处理群聊消息
        elif message_type == 'group':
            message_handler_thread.message_handler(raw_message, gid=group_id, qid=sender_id)
        # 返回响应
        return 'OK'
    
    @app.route(f'/api/v1/service_message', methods=['POST'])
    def register_service_message():
        '''
        将服务程序传回的信息转发回信息源
        '''
        data = request.get_json()
        message = data.get('message')
        gid = data.get('gid')
        qid = data.get('qid')
        from DBot_SDK.utils import send_message_to_cqhttp
        send_message_to_cqhttp(message, gid, qid)
        return jsonify({'message': 'OK'}), 200

    # 定义心跳路径
    @app.route('/api/v1/heartbeat/<name>')
    def heartbeat(name):
        # 处理心跳请求，并返回相应
        heartbeat_manager.register(name)
        return 'Heartbeat OK for service {}'.format(name)

    @app.route('/health')
    def health_check():
        return 'OK'
