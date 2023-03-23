from flask import request

def route_registration(app):
<<<<<<<< HEAD:dzmicro/api/server_routes.py
    from dzmicro.conf import RouteInfo
    from dzmicro.conf import Authority
    from dzmicro.utils import task_thread
========
    from dbot.conf import RouteInfo
    from dbot.conf import Authority
    from dbot.utils import task_thread
>>>>>>>> 5db5c8d65bf9963ee23a28ac253e0f4045b1a5f0:example/dbot/api/server_routes.py
    @app.route(f'/api/v1/receive_command', methods=['POST'])
    def receive_command():
        data = request.get_json()
        command = data.get('command')
        args = data.get('args')
        source_id = data.get('source_id')
        is_user_call = data.get('is_user_call', True)
        permission = True
        if is_user_call:
            permission = Authority.check_command_permission(command=command, source_id=source_id)  
        if permission:
            task_thread.add_task(command=command, args=args, source_id=source_id)
        return {'permission': permission}
    
    @app.route('/health')
    def health_check():
        return 'OK'
