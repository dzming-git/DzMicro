from flask import request

def route_registration(app):
    from DBot_SDK.conf import RouteInfo
    from DBot_SDK.conf import Authority
    from DBot_SDK.utils import task_thread
    receive_command_endpoint = RouteInfo.get_service_endpoint('receive_command')
    @app.route(f'/{receive_command_endpoint}', methods=['POST'])
    def receive_command():
        data = request.get_json()
        command = data['command']
        args = data['args']
        gid = data['gid']
        qid = data['qid']
        permission = Authority.check_command_permission(command=command, group_id=gid, qq_id=qid)
        if permission:
            task_thread.add_task(command=command, args=args, gid=gid, qid=qid)
        return {'permission': permission}
    
    @app.route('/health')
    def health_check():
        return 'OK'
