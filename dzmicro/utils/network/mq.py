import threading
import pika
import json
from pika.adapters import blocking_connection
from typing import Callable, Dict, Tuple

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
    
    def set_consumer(self, queue_name: str, task_handler: Callable[[Dict[str, any]], Tuple[bool, Dict[str, any]]], attempt_max = -1, reply: bool = False):
        def callback(ch: blocking_connection.BlockingChannel, method, props, body):
            task = json.loads(body)
            ok, result_dict = task_handler(task)
            if ok:
                if reply:
                    ch.basic_publish(exchange='',
                                    routing_key=f'{queue_name}_reply',
                                    body=json.dumps(result_dict))
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
    
    def send_task(self, task: Dict[str, any], queue_name: str, reply=None) -> None:
        while True:
            try:
                self._channel.basic_publish(
                    exchange='',
                    routing_key=queue_name,
                    body=json.dumps(task),
                    properties=pika.BasicProperties(
                        reply_to=reply,
                        # correlation_id=corr_id,
        ),
                )
                break
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
