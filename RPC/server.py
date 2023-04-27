from time import sleep
import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'),
)
channel = connection.channel()
channel.queue_declare(queue='rpc-queue')


def callable(ch, method, properties, body: str):
    print('Processing requests...')
    number = int(body) if body.isdigit() else 1
    sleep(3)
    response = str(number + 1)
    channel.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id,
        ),
        body=response,
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue='rpc-queue',
    on_message_callback=callable,
)
print('Waiting for client...')
channel.start_consuming()
