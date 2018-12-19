import asyncio
import logging
from logging.config import fileConfig

from service.mongodb.db_layer import DBLayer


def __init_logger__():
    fileConfig('logging.conf')
    logger = logging.getLogger()
    logger.info("Logger was initialized.")


__init_logger__()
io_loop = asyncio.get_event_loop()
db_layer = DBLayer(io_loop)

