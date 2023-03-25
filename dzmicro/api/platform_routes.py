# platform_routes.py
from flask import request, jsonify, Flask

def platform_route_registration(app: Flask) -> None:
    @app.route(f'/api/v1/service_message', methods=['POST'])
    def register_service_message():
        '''
        将服务程序传回的信息转发回信息源
        '''
        data = request.get_json()
        message = data.get('message')
        source_id = data.get('source_id')
        from dzmicro.utils import MessageSender
        message_sender = MessageSender()
        message_sender.send_message_to_source(message, source_id)
        return jsonify({'message': 'OK'}), 200

    # 定义心跳路径
    @app.route('/api/v1/heartbeat/<name>')
    def heartbeat(name: str):
        # 处理心跳请求，并返回相应
        from dzmicro.utils.network import HeartbeatManager
        heartbeat_manager = HeartbeatManager()
        heartbeat_manager.register(name)
        return 'Heartbeat OK for service {}'.format(name)

    @app.route('/health')
    def health_check():
        return 'OK'
