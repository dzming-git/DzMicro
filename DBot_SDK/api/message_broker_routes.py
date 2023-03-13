# message_broker_routes.py
from flask import request, jsonify
from DBot_SDK.app.message_handler.bot_commands import BotCommands
from DBot_SDK.app.message_handler.service_registry import serviceRegistry
from DBot_SDK.utils.message_sender import Msg_struct, send_message_to_cqhttp
from DBot_SDK.app.message_handler.message_handler import message_handler_thread

def message_broker_route_registration(app):
    @app.route('/', methods=['POST'])
    def handle_message():
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

    from DBot_SDK.conf import RouteInfo
    service_commands_endpoint = RouteInfo.get_message_broker_endpoint('service_commands')
    @app.route(f'/{service_commands_endpoint}', methods=['POST'])
    def register_service_commands():
        data = request.get_json()
        service_name = data.get('service_name')
        commands = data.get('commands')
        if service_name and commands:
            for command in commands:
                BotCommands.add_commands(command, service_name)            
            return jsonify({'message': 'Bot commands registered successfully'}), 200
        else:
            return jsonify({'message': 'Invalid request'}), 400
    
    service_message_endpoint = RouteInfo.get_message_broker_endpoint('service_message')
    @app.route(f'/{service_message_endpoint}', methods=['POST'])
    def register_service_message():
        data = request.get_json()
        message = data.get('message')
        gid = data.get('gid')
        qid = data.get('qid')
        msg_struct = Msg_struct(gid=gid, qid=qid, msg=message)
        send_message_to_cqhttp(msg_struct)
        return jsonify({'message': 'OK'}), 200
    
    service_endpoints_endpoint = RouteInfo.get_message_broker_endpoint('service_endpoints')
    @app.route(f'/{service_endpoints_endpoint}', methods=['POST'])
    def register_service_endpoints():
        data = request.get_json()
        service_name = data.get('service_name')
        endpoints_info = data.get('endpoints_info')
        if service_name and endpoints_info:
            usages = list(endpoints_info.keys())
            for usage in usages:
                endpoint = endpoints_info[usage]
                serviceRegistry.add_service_endpoint(service_name, usage, endpoint)
            return jsonify({'message': 'Bot commands registered successfully'}), 200
        else:
            return jsonify({'message': 'Invalid request'}), 400
    
    @app.route('/health')
    def health_check():
        return 'OK'
