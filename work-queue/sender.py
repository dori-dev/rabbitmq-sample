import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'),
)
channel = connection.channel()
channel.queue_declare(queue='first', durable=True)

message = "Hi, I am Mohammad Dori!"
channel.basic_publish(
    exchange='',
    routing_key='first',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,
        headers={
            'name': 'Mohammad Dori',
        },
    ),
)
print('Message sended successfully!')

connection.close()
