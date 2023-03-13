from DBot_SDK.utils.service_discovery import consul_client

def register_consul(app, name, port):
    '''
    服务开启前,注册consul
    '''
    id = consul_client.register_service(name, port, [])
    app.config.update({'id': id})

def deregister_service(app):
    '''
    服务结束后,注销consul
    '''
    id = app.config['id']
    consul_client.deregister_service(id)
        
def discover_message_broker(service_name):
    """
    发现机器人消息代理
    """
    services = consul_client.discover_services(service_name)
    if services:
        from DBot_SDK.conf import RouteInfo
        message_broker = services[0]
        RouteInfo.update_message_broker(ip=message_broker[0], port=message_broker[1])
        return True
    print('消息代理未开启')
    return False

def message_broker_endpoints_upload():
    """
    消息代理专用
    将自己的endpoint上传至consul的KV中
    """
    from DBot_SDK.conf import RouteInfo
    service_endpoints_info = RouteInfo.get_message_broker_endpoints_info()
    message_broker_consul_key = RouteInfo.get_message_broker_consul_key('message_broker_endpoints')
    message_broker_endpoints_dict = {
        message_broker_consul_key: service_endpoints_info
    }
    consul_client.update_key_value(message_broker_endpoints_dict)
