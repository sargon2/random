
import unittest
import pika

class TestRabbitMQ(unittest.TestCase):
    def test_receive(self):
        # send
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue="test")
        channel.basic_publish(exchange='', routing_key='test', body='message body')
        connection.close()

        # receive
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue="test")

        (method_frame, header_frame, body) = channel.basic_get(queue="test")
        self.assertEquals("message body", body)
