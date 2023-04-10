from dzmicro.utils.singleton import singleton
from typing import Dict, Union

@singleton
class ServerSharedInfo:
    def __init__(self) -> None:
        from dzmicro.utils.listener_manager import ListenerManager
        self.listener_manager = ListenerManager()

class ServerUniqueInfo:
    def __init__(self, uuid: str, is_paltform: bool = False) -> None:
        from dzmicro.app import ServerThread
        from dzmicro.app.message_handler.bot_commands import BotCommands
        from dzmicro.app.message_handler.message_handler import MessageHandlerThread
        from dzmicro.app.services.service import FuncDict
        from dzmicro.conf import Authority, ConsulInfo, MQInfo, RouteInfo
        from dzmicro.utils.network import ConsulClient, HeartbeatManager, MessageSender, MQThread, MQReplyThread, WatchKVThread
        self.uuid = uuid
        self.is_paltform = is_paltform
        self.server_thread = ServerThread(uuid, is_paltform)
        self.bot_commands = BotCommands(uuid, is_paltform)
        self.message_handler_thread = MessageHandlerThread(uuid, is_paltform)
        self.func_dict = FuncDict(uuid, is_paltform)
        self.authority = Authority(uuid, is_paltform)
        self.consul_info = ConsulInfo(uuid, is_paltform)
        self.mq_info = MQInfo(uuid, is_paltform)
        self.route_info = RouteInfo(uuid, is_paltform)
        self.consul_client = ConsulClient(uuid, is_paltform)
        self.watch_kv_thread = WatchKVThread(uuid, is_paltform)
        self.heartbeat_manager = HeartbeatManager(uuid, is_paltform)
        self.message_sender = MessageSender(uuid, is_paltform)

        # 保证MQ线程安全，通道不能跨线程使用
        self.producer_mq = MQThread(uuid, is_paltform)         # 生产者，发送消息，不需要启动线程
        self.consumer_mq_thread = MQThread(uuid, is_paltform)  # 消费者，处理消息，需要启动线程

        self.mq_replay_thread = MQReplyThread(uuid, is_paltform)

@singleton
class ServerManager:
    def __init__(self) -> None:
        self.server_shared_info = ServerSharedInfo()
        self.servers: Dict[str, ServerUniqueInfo] = {}
    
    def add_server(self, uuid: str, is_paltform: bool = False) -> bool:
        if uuid in self.servers:
            return False
        else:
            self.servers[uuid] = ServerUniqueInfo(uuid, is_paltform)
            return True
    
    def load_server(self, uuid: str):
        server = self.servers.get(uuid, None)
        if server is None:
            return
        
        # Authority
        server.authority.set_server_unique_info()
        
        # ConsulClient
        server.consul_client.set_server_unique_info()
        for kv in server.consul_info.get_kvs():
            server.consul_client.update_key_value(kv)

        # WatchKVThread
        server.watch_kv_thread.set_server_unique_info()
        server.watch_kv_thread.start()

        # ServerThread
        server.server_thread.set_server_unique_info()
        server.server_thread.start()

        # MessageHandlerThread
        server.message_handler_thread.set_server_unique_info()
        server.message_handler_thread.start()

        # MessageSender
        server.message_sender.set_server_unique_info()

        # HeartbeatManager
        server.heartbeat_manager.set_server_unique_info()
        server.heartbeat_manager.start()

        # MQThread
        server.consumer_mq_thread.set_server_unique_info()
        server.consumer_mq_thread.create_channel()
        server.producer_mq.set_server_unique_info()
        server.producer_mq.create_channel()
        if server.is_paltform:
            from dzmicro.api.platform.platform_consumer import set_consumer
        else:
            from dzmicro.api.server.server_consumer import set_consumer
        set_consumer(server.consumer_mq_thread)
        server.consumer_mq_thread.start()
        
        # MQReplyThread
        server.mq_replay_thread.start()

        return True

    def get_server_unique_info(self, uuid: str) -> Union[ServerUniqueInfo, None]:
        if uuid in self.servers:
            return self.servers[uuid]
        else:
            return None
    
    def get_server_shared_info(self) -> ServerSharedInfo:
        return self.server_shared_info

# 单例模式
singleton_server_manager = ServerManager()
