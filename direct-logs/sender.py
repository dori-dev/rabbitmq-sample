import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'),
)
channel = connection.channel()

channel.exchange_declare(
    exchange='direct_logs',
    exchange_type='direct',
)

messages = {
    'info': 'This is a INFO message.',
    'error': 'This is an ERROR message.',
    'warning': 'This is a WARNING messages.'
}
for key, value in messages.items():
    channel.basic_publish(
        exchange='direct_logs',
        routing_key=key,
        body=value,
    )

connection.close()
