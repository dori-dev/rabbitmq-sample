from time import sleep

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties


def callback(
        ch: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body):
    print(f'Received {body}')
    print(properties.headers)
    sleep(9)
    print('Done')
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'),
)
channel = connection.channel()
channel.queue_declare(queue='first', durable=True)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue='first',
    on_message_callback=callback,
)
print('Waiting for message, press ctrl-c to exit...')

channel.start_consuming()
