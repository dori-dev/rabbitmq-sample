import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'),
)
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

messages = {
    'error.warning.important': 'This is an important message',
    'info.debug.unimportant': 'This is an unimportant message',
}

for key, value in messages.items():
    channel.basic_publish(exchange='topic_logs', routing_key=key, body=value)

print('The logs was sended.')
connection.close()
