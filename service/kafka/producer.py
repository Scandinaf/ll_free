import json
import logging


class Producer:
    def __init__(self, producer, topic_name):
        self.producer = producer
        self.topic_name = topic_name
        self.module_logger = logging.getLogger()

    async def send_message(self, message):
        try:
            await self.producer.send_and_wait(
                self.topic_name, json.dumps(
                    message.build_kafka_message()).encode('UTF-8'))
        except Exception as exp:
            self.module_logger.error("Exception : {}".format(exp))
