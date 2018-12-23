import logging


class Producer:
    def __init__(self, producer, topic_name):
        self.producer = producer
        self.topic_name = topic_name
        self.module_logger = logging.getLogger()

    async def send_message(self, message):
        try:
            await self.producer.send_and_wait(
                self.topic_name, self.__get_message__(message).encode('UTF-8'))
        except Exception as exp:
            self.module_logger.error("Exception : {}".format(exp))

    def __get_message__(self, message):
        if isinstance(message, str):
            return message
        else:
            return message.get_kafka_message()
