import threading
import pika
import json
import uuid
import time
import copy
from pika.adapters import blocking_connection
from pika.spec import BasicProperties
from typing import Callable, Dict, Tuple
from dzmicro.utils.singleton import singleton
from dzmicro.app.message_handler.error_handler import connect_error_handler

@singleton
class MQReplyThread(threading.Thread):
    def __init__(self, timeout=1) -> None:
        super().__init__(name='MQReplyThread')
        self.reply_dict = {}
        self.timeout = timeout
        self._lock = threading.Lock()
        self.started = False
        self.start()
    
    def wait_reply(self, correlation_id: str, task: Dict[str, any], queue_name: str, wait: bool = False):
        with self._lock:
            self.reply_dict[correlation_id] = {
                'taks': task,
                'queue_name': queue_name,
                'wait_time': 0,
                'reply': None,
                'timeout': False
            }
        if wait:
            while True:
                reply = self.reply_dict.get(correlation_id, {}).get('reply', None)
                if reply is not None:
                    return reply
                if self.reply_dict[correlation_id]['timeout'] is True:
                    return None
                time.sleep(0.01)
    
    def ack_reply(self, correlation_id: str, reply: any):
        if correlation_id in self.reply_dict:
            with self._lock:
                self.reply_dict[correlation_id]['reply'] = reply
    
    def start(self):
        if self.started:
            pass
        else:
            self.started = True
            super().start()

    def run(self):
        time_interval = 0.1
        while True:
            reply_dict_temp = copy.deepcopy(self.reply_dict)
            for correlation_id, _dict in reply_dict_temp.items():
                if _dict.get('wait_time', 0) > self.timeout and self.reply_dict.get('reply', None) is None:
                    with self._lock:
                        self.reply_dict[correlation_id]['timeout'] = True
                else:
                    wait_time = self.reply_dict.get('wait_time', 0)
                    wait_time += time_interval
    
                    with self._lock:
                        self.reply_dict[correlation_id]['wait_time'] = wait_time
            time.sleep(time_interval)


class MQThread(threading.Thread):
    def __init__(self) -> None:
        super().__init__(name='MQThread')
        self._credentials = None
        self._channel = None
    
    def set_credentials(self, username: str, password: str) -> None:
        self._credentials = pika.PlainCredentials(username,  password)
    
    def create_channel(self, host: str = 'localhost') -> None:
        if self._credentials is None:
            print('请先set_credentials')
            return
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host, credentials=self._credentials, virtual_host='/'))
        self._channel = connection.channel()
        self._channel.basic_qos(prefetch_count=1)
    
    def declare_queue(self, queue_name: str) -> None:
        dead_queue_name = f'{queue_name}_dead'
        self._channel.queue_declare(queue=queue_name, durable=True, arguments={
            'x-dead-letter-exchange': '',
            'x-dead-letter-routing-key': dead_queue_name,
            'x-message-ttl': 10000
        })
        self._channel.queue_declare(queue=dead_queue_name, durable=True)
        reply_queue_name = f'{queue_name}_reply'
        self._channel.queue_declare(queue=reply_queue_name, durable=True)
    
    def set_consumer(self, 
                     queue_name: str, 
                     task_handler: Callable[[Dict[str, any], BasicProperties], Tuple[bool, Dict[str, any], BasicProperties]], 
                     attempt_max = -1, 
                     reply: bool = False):
        def callback(ch: blocking_connection.BlockingChannel, method, props: BasicProperties, body):
            task = json.loads(body)
            ok, result_dict, props_send = task_handler(task, props)
            if ok:
                if reply:
                    ch.basic_publish(exchange='',
                                    routing_key=f'{queue_name}_reply',
                                    body=json.dumps(result_dict),
                                    properties=props_send)
            else:
                attempts = 0
                rejects = []
                if props.headers:
                    attempts = props.headers.get('x-attempts-header', 0)
                    rejects = props.headers.get('x-rejects-header', [])
                if attempt_max > 0 and attempts > attempt_max:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                    return
                if self._channel.channel_number in rejects:
                    pass
                else:
                    rejects.append(self._channel.channel_number)
                    attempts += 1
                ch.basic_publish(exchange='',
                        routing_key='cal',
                        body=json.dumps(task),
                        properties=pika.BasicProperties(
                            reply_to=props.reply_to,
                            delivery_mode=2, # 消息持久化
                            headers={
                                'x-origin-queue': queue_name,
                                'x-attempts-header': attempts,
                                'x-rejects-header': rejects
                            }
                        ))
            ch.basic_ack(delivery_tag=method.delivery_tag)
        self._channel.basic_consume(queue=queue_name, on_message_callback=callback)
    
    def send_task(self, task: Dict[str, any], queue_name: str) -> str:
        while True:
            try:
                correlation_id = str(uuid.uuid4())
                self._channel.basic_publish(
                    exchange='',
                    routing_key=queue_name,
                    body=json.dumps(task),
                    properties=pika.BasicProperties(correlation_id = correlation_id,
                                                    delivery_mode=2),
                )
                return correlation_id
            except Exception as e:
                print(e)
    
    def get_queue(self):
            return self._channel.method.queue
    
    def run(self) -> None:
        self._channel.start_consuming()

def create_mq() -> MQThread:
    from dzmicro.conf import MQInfo
    mq_info = MQInfo()
    mq_thread = MQThread()
    username, password = mq_info.get_uesrinfo()
    mq_thread.set_credentials(username, password)
    mq_thread.create_channel()
    return mq_thread
