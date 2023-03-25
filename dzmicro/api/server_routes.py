from flask import request, Flask

def route_registration(app: Flask) -> None:
    from dzmicro.conf import Authority
    from dzmicro.utils import TaskThread
    @app.route(f'/api/v1/receive_command', methods=['POST'])
    def receive_command():
        data = request.get_json()
        command = data.get('command')
        args = data.get('args')
        source_id = data.get('source_id')
        is_user_call = data.get('is_user_call', True)
        permission = True
        if is_user_call:
            authority = Authority()
            permission = authority.check_command_permission(command=command, source_id=source_id)  
        if permission:
            task_thread = TaskThread()
            task_thread.add_task(command=command, args=args, source_id=source_id)
        return {'permission': permission}
    
    @app.route('/health')
    def health_check():
        return 'OK'
