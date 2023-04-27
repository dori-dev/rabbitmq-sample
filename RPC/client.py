from uuid import uuid4
import pika


class Sender:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'),
        )
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = queue.method.queue
        self.response = None
        self.corr_id = None
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = body
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def call(self, number):
        self.corr_id = uuid4().hex
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc-queue',
            properties=pika.BasicProperties(
                reply_to=self.queue_name,
                correlation_id=self.corr_id,
            ),
            body=str(number),
        )
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


if __name__ == '__main__':
    send = Sender()
    result = send.call(13)
    print(result)
