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
    _listens = []
    
    def update_listens(self, service_name, command, gid, qid, should_listen):
        #TODO 删除监听还没写
        if should_listen:
            should_add = True
            for listen in self._listens:
                if \
                    service_name == listen.get('service_name') and \
                    command == listen.get('command') and \
                    gid == listen.get('gid'):
                    if (gid is None and qid == listen.get('qid')) or gid:
                        should_add = False
            if should_add:
                self._listens.append({
                    'service_name': service_name,
                    'command': command,
                    'gid': gid,
                    'qid': qid
                })
            else:
                pass
    
    def get_listens(self):
        '''
        获取目前监听状态的服务和申请监听的指令
        '''
        return self._listens

listener_manager = ListenerManager()
