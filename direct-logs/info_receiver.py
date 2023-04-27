import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'),
)
channel = connection.channel()

channel.exchange_declare(
    exchange='direct_logs',
    exchange_type='direct',
)

queue = channel.queue_declare(queue='', exclusive=True)
queue_name = queue.method.queue

severities = [
    'info',
    'warning',
    'error',
]
for severity in severities:
    channel.queue_bind(
        exchange='direct_logs',
        queue=queue_name,
        routing_key=severity,
    )


def callback(channel, method, properties, body):
    severity = method.routing_key.upper()
    print(f'{severity}: {body.decode()}')


print('Waiting for message...')
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True,
)

channel.start_consuming()
