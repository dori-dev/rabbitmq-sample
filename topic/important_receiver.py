import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'),
)
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

queue = channel.queue_declare('', exclusive=True)
queue_name = queue.method.queue

binding_key = '*.*.important'
channel.queue_bind(
    exchange='topic_logs',
    queue=queue_name,
    routing_key=binding_key,
)


def callback(channel, method, properties, body: bytes):
    with open('important.log', 'a') as log_file:
        log_file(f'{body.decode()}\n')


print('Waiting for log...')
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True,
)

channel.start_consuming()
