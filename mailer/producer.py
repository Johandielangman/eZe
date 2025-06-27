#!/usr/bin/env python3
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: June 2025
# Description: Simple RabbitMQ message producer
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

import pika
from loguru import logger


def send_message(message, queue_name='task_queue'):
    """Send a single message to the queue"""
    try:
        # Create connection
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        # Declare the queue (same as consumer)
        channel.queue_declare(queue=queue_name, durable=True)
        # Publish message
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )
        logger.info(f"Sent: {message}")
        connection.close()
        return True
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        return False
