class ListenerManager:
    '''
    _listens = [
        {
            'service_name':
            'command':
            'gid':
            'qid':
        }
    ]

    '''
    _listeners = []
    
    def update_listeners(self, service_name, keyword, command, ip, port, gid, qid, should_listen):
        #TODO 删除监听还没写
        #TODO 如果同一个服务在多太设备上运行，只有一个服务可以开启监听，待完善
        #TODO 如果同一个服务在多太设备上运行，执行监听任务的服务意外关闭，需要将监听切换到其他设备上
        if should_listen:
            should_add = True
            for listener in self._listeners:
                # 相同服务名、相同关键词、同样指令、同人私聊或同群群聊，则判定为同一个监听者
                if \
                    service_name == listener.get('service_name') and \
                    keyword == listener.get('keyword') and \
                    command == listener.get('command') and \
                    gid == listener.get('gid'):
                    if (gid is None and qid == listener.get('qid')) or gid == listener.get('gid'):
                        should_add = False
            if should_add:
                self._listeners.append({
                    'service_name': service_name,
                    'keyword': keyword,
                    'command': command,
                    'ip': ip,
                    'port': port,
                    'gid': gid,
                    'qid': qid
                })
            else:
                pass
    
    def get_listeners(self):
        '''
        获取目前监听状态的服务和申请监听的指令
        '''
        return self._listeners

listener_manager = ListenerManager()
