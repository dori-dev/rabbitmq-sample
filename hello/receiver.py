import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'),
)


def hello_callback(ch, method, properties, body):
    print(f"Received {body}")


channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_consume(
    queue='hello',
    on_message_callback=hello_callback,
    auto_ack=True,
)

print('Waiting for message, press ctrl-c to exit...')
channel.start_consuming()
