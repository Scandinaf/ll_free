import logging

import kafka

from bootstrapper import __init_logger__, __init_io_loop__, __init_db_layer__
from service.word_service_consumer import WordServiceConsumer

if __name__ == '__main__':
    __init_logger__()
    module_logger = logging.getLogger()
    loop = __init_io_loop__()
    db_layer = __init_db_layer__(loop)
    module_logger.info('Consumer was started!!!')
    try:
        consumer = WordServiceConsumer(db_layer, "ll_free.full_model", loop)
    except kafka.errors.ConnectionError as kafka_exp:
        module_logger.error("Exception : {}".format(kafka_exp))
        print("Could you please check the connection to Kafka.")
    else:
        loop.run_until_complete(consumer.run_consumer())
    loop.close()