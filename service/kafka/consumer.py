import logging
from abc import abstractmethod, ABC

from aiokafka import AIOKafkaConsumer


class Consumer(ABC):
    def __init__(self, topic_name, loop, kafka_host='127.0.0.1', kafka_port=9092):
        self.module_logger = logging.getLogger()
        self.consumer = AIOKafkaConsumer(topic_name,
                                         loop=loop,
                                         bootstrap_servers='{0}:{1}'.format(kafka_host, kafka_port))
        loop.run_until_complete(self.consumer.start())

    @abstractmethod
    def __handler__(self, msg):
        pass

    async def run_consumer(self):
        try:
            async for msg in self.consumer:
                await self.__handler__(msg)
        except Exception as exp:
            self.__unexpected_exception__(exp)
        finally:
            await self.consumer.stop()

    def __unexpected_exception__(self, exp):
        self.module_logger.error("Exception : {}".format(exp))
