# platform_routes.py
from flask import request, jsonify, Flask

def route_registration(app: Flask) -> None:
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
