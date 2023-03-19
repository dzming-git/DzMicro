from DBot_SDK.utils.judge_same_listener import judge_same_listener

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
    def __init__(self):
        self._listeners = []
    
    # 平台程序使用
    def update_listeners(self, consul_listeners, is_rm=False):
        #TODO 如果同一个服务在多设备上运行，只有一个服务可以开启监听，待完善
        #TODO 如果同一个服务在多设备上运行，执行监听任务的服务意外关闭，需要将监听切换到其他设备上
        for consul_listener in consul_listeners:
            should_add = True
            should_rm = False
            for i, listener in enumerate(self._listeners):
                if judge_same_listener(listener=listener,
                                    service_name=consul_listener.get('service_name'),
                                    keyword=consul_listener.get('keyword'),
                                    command=consul_listener.get('command'),
                                    gid=consul_listener.get('gid'),
                                    qid=consul_listener.get('qid')):
                        should_add = not is_rm
                        should_rm = is_rm
            if should_add:
                self._listeners.append(consul_listener)
            if should_rm:
                self._listeners.pop(i)
    
    def get_listeners(self):
        '''
        获取目前监听状态的服务和申请监听的指令
        '''
        # 创建一个空列表，用于存储具有 should_listen 属性且其值为 True 的对象
        should_listen_listeners = []

        # 遍历 self._listeners 列表中的每个元素
        for listener in self._listeners:
            # 检查该元素是否具有 should_listen 属性，并且其值为 True
            if listener.get('should_listen', False):
                # 如果满足条件，则将该元素添加到 should_listen_listeners 列表中
                should_listen_listeners.append(listener)

        # 返回 should_listen_listeners 列表
        return should_listen_listeners


listener_manager = ListenerManager()
