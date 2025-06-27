# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: June 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // STANDARD IMPORT // ===============

import signal
import threading
import time
import traceback
from typing import (
    List,
    Optional
)


# =============== // MODULE IMPORT // ===============

import constants as c

# =============== // LIBRARY IMPORT // ===============

from loguru import logger
import pika

# =============== // SETUP // ===============

LOG_FORMAT: str = "{time} | {level} | {name}:{module}:{function}:{line} | {message}"
shutdown_event: threading.Event = threading.Event()
NUM_WORKERS: int = 2

logger.add(
    f"{c.LOG_DIR}/mailer.log",
    level="DEBUG",
    rotation="20 MB",
    retention="7 days",
    compression="zip",
    format=LOG_FORMAT
)

# =============== // SIGNAL HANDLER // ===============


def signal_handler(
    signum: int,
    frame: Optional[signal.FrameType]
):
    logger.info(f"Signal {signum} received, shutting down gracefully...")
    shutdown_event.set()


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# =============== // MESSAGE PROCESSOR // ===============


def message_handler(
    ch: pika.adapters.blocking_connection.BlockingChannel,
    method: pika.spec.Basic.Deliver,
    properties: pika.spec.BasicProperties,
    body: bytes,
    worker_id: int
) -> None:
    """Process a single message from RabbitMQ"""
    try:
        message: str = body.decode('utf-8')
        logger.info(f"Worker {worker_id} processing: {message}")

        time.sleep(0.1)
        logger.debug(f"Worker {worker_id} finished processing message: {message}")

        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.debug(f"Worker {worker_id} completed processing")

    except Exception as e:
        logger.error(f"Worker {worker_id} error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


# =============== // WORKER THREAD // ===============

def worker_thread(
    worker_id: int,
    queue_name='task_queue'
):
    connection = None
    try:
        connection: pika.BlockingConnection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost'
            )
        )
        channel: pika.adapters.blocking_connection.BlockingChannel = connection.channel()

        channel.queue_declare(queue=queue_name, durable=True)

        channel.basic_qos(prefetch_count=1)

        logger.info(f"Worker {worker_id} started, waiting for messages...")

        def callback(
            ch: pika.adapters.blocking_connection.BlockingChannel,
            method: pika.spec.Basic.Deliver,
            properties: pika.spec.BasicProperties,
            body: bytes
        ) -> None:
            if shutdown_event.is_set():
                return
            message_handler(
                ch=ch,
                method=method,
                properties=properties,
                body=body,
                worker_id=worker_id
            )

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback
        )

        # ====> Keep consuming until shutdown
        while not shutdown_event.is_set():
            try:
                # ====>  Use timeout to make it responsive to shutdown
                connection.process_data_events(time_limit=1)
            except pika.exceptions.AMQPTimeoutError:
                continue
    except Exception as e:
        logger.error(f"Worker {worker_id} encountered error: {e}")
        logger.error(traceback.format_exc())
    finally:
        if connection and not connection.is_closed:
            connection.close()
        logger.info(f"Worker {worker_id} shut down")


# =============== // MAIN FUNCTION // ===============

def main():
    logger.info(f"Starting mailer with {NUM_WORKERS} workers 📪📫📬")

    workers: List[threading.Thread] = []

    try:
        for i in range(NUM_WORKERS):
            logger.info(f"Starting worker {i + 1}...")
            worker = threading.Thread(
                target=worker_thread,
                args=(i + 1,),
                name=f"Worker-{i + 1}"
            )
            worker.daemon = True
            worker.start()
            workers.append(worker)

        # ====> READY FOR ACTION 🐇
        logger.info("All workers started, waiting for messages...")

        # ====> BLOCK UNTIL SHUTDOWN SIGNAL
        shutdown_event.wait()

        # ====> SHUTDOWN PROCEDURE
        logger.info("Shutdown signal received, stopping workers...")
        for worker in workers:
            worker.join(timeout=5)

        # ====> DEBUG
        alive_workers = [w for w in workers if w.is_alive()]
        if alive_workers:
            logger.warning(f"{len(alive_workers)} workers didn't shut down gracefully")
    except KeyboardInterrupt:
        logger.warning("Received KeyboardInterrupt, shutting down...")
        shutdown_event.set()
    except Exception as e:
        logger.error(f"Main thread error: {e}")
        logger.error(traceback.format_exc())
    logger.info("bye 👋")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        logger.error(traceback.format_exc())
