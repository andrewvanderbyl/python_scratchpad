#!/usr/bin/env python
"""Simple RMQ Receive."""
import pika
import sys
import os


def main():
    """
    Rabbitmq consume main body.

    Parameters
    ----------
    None. This is simply a debug receiver.

    Return: None
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="MsgQueue")

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue="MsgQueue", on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
