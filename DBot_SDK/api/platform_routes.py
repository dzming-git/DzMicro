# platform_routes.py
from flask import request, jsonify
from DBot_SDK.utils.network import heartbeat_manager

def platform_route_registration(app):
    @app.route('/', methods=['POST'])
    def handle_message():
        '''
        将信息源的信息转发至服务程序
        '''
        from DBot_SDK.app.message_handler.message_handler import message_handler_thread
        # 获取消息体
        message = request.json
        print(message)
        # 获取source_id
        qid = message.get('sender', {}).get('user_id')
        gid = message.get('group_id')
        source_id = [gid, qid]
        # 获取原始消息内容
        raw_message = message.get('raw_message')
        message_handler_thread.message_handler(raw_message, source_id)
        # 返回响应
        return 'OK'
    
    @app.route(f'/api/v1/service_message', methods=['POST'])
    def register_service_message():
        '''
        将服务程序传回的信息转发回信息源
        '''
        data = request.get_json()
        message = data.get('message')
        source_id = data.get('source_id')
        from DBot_SDK.utils import send_message_to_source
        send_message_to_source(message, source_id)
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
