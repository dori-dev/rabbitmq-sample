import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'),
)
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

queue = channel.queue_declare('', exclusive=True)
queue_name = queue.method.queue

binding_key = '#.unimportant'
channel.queue_bind(
    exchange='topic_logs',
    queue=queue_name,
    routing_key=binding_key,
)


def callback(channel, method, properties, body):
    print(body)


print('Waiting for log...')
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True,
)

channel.start_consuming()
