import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

queue = channel.queue_declare(queue='', exclusive=True)
queue_name = queue.method.queue

channel.queue_bind(
    exchange='direct_logs',
    queue=queue_name,
    routing_key='error',
)


def callback(channel, method, properties, body):
    with open('error_logs.log', 'a') as log_file:
        log_file.write(f'{body.decode()}\n')


print('Waiting for logs...')
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True,
)
channel.start_consuming()
