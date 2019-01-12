import json

from service.audio_record_loader import AudioRecordLoader
from service.kafka.consumer import Consumer


class WordServiceConsumer(Consumer):
    def __init__(self, db_layer, topic_name, loop, kafka_host='127.0.0.1', kafka_port=9092):
        Consumer.__init__(self, topic_name, loop, kafka_host, kafka_port)
        self.db_layer = db_layer
        self.audio_loader_service = AudioRecordLoader(dir_path="E:\\dictionary\\")

    async def __handler__(self, msg):
        self.module_logger.info('Received message: {}'.format(msg))
        try:
            msg_dict = json.loads(msg.value.decode("UTF-8"))
            word = msg_dict['word']
            if await self.db_layer.word.record_is_exists(word):
                sound_record_path = await self.audio_loader_service.load_audio_record(word)
                await self.db_layer.word.update_audio_record_path(word, sound_record_path)
        except Exception as exp:
            return self.__unexpected_exception__(exp)
