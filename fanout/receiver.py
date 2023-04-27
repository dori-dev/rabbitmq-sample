from time import sleep
import pika
from pika.frame import Method

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'),
)
channel = connection.channel()

channel.exchange_declare(
    exchange='logs',
    exchange_type='fanout',
)
queue: Method = channel.queue_declare(queue='', exclusive=True)
queue_name = queue.method.queue
channel.queue_bind(
    exchange='logs',
    queue=queue_name,
)


def callback(ch, method, properties, body):
    sleep(3)
    print("Received", {body})
    print("Queue", queue_name)


print('Waiting for logs')
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True,
)
channel.start_consuming()
