from flask import request

def route_registration(app):
    from DBot_SDK.conf import RouteInfo
    from DBot_SDK.conf import Authority
    from DBot_SDK.utils import task_thread
    @app.route(f'/api/v1/receive_command', methods=['POST'])
    def receive_command():
        data = request.get_json()
        command = data.get('command')
        args = data.get('args')
        gid = data.get('gid')
        qid = data.get('qid')
        is_user_call = data.get('is_user_call', True)
        permission = True
        if is_user_call:
            permission = Authority.check_command_permission(command=command, group_id=gid, qq_id=qid)  
        if permission:
            task_thread.add_task(command=command, args=args, gid=gid, qid=qid)
        return {'permission': permission}
    
    @app.route('/health')
    def health_check():
        return 'OK'
