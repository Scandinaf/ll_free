import asyncio
import logging
from logging.config import fileConfig

from aiokafka import AIOKafkaProducer

from service.mongodb.db_layer import DBLayer


def __init_logger__():
    fileConfig('logging.conf')
    logger = logging.getLogger()
    logger.info("Logger was initialized.")


def __init_io_loop__():
    return asyncio.get_event_loop()


def __init_db_layer__(loop):
    return DBLayer(loop)


def __init_producer__(loop):
    producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers='{0}:{1}'.format("127.0.0.1", 9092))
    loop.run_until_complete(producer.start())
    return producer
