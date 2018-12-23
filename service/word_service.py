import logging
from json import JSONDecodeError

from jsonschema import ValidationError

from model.error import Error
from model.word import Word
from model.word_kafka_message import WordKafkaMessage
from service.kafka.producer import Producer
from utils.helper import remove_file, validate_json, exclude_json_fields


class WordService:
    def __init__(self, db_layer, producer):
        self.db_layer = db_layer
        self.producer = Producer(producer, "ll_free.full_model")
        self.module_logger = logging.getLogger()

    async def reload_translation(self, word):
        try:
            if not await self.db_layer.word.record_is_exists(word):
                return Error("Word not found!!!")
            await self.producer.send_message(WordKafkaMessage(word))
            return "The audio recording will be updated!!!"
        except Exception as exp:
            return self.__unexpected_exception__(exp)

    async def get_word(self, word):
        try:
            db_record_dict = await self.db_layer.word.find_one_by_word(word)
        except Exception as exp:
            return self.__unexpected_exception__(exp)
        else:
            if db_record_dict is None:
                return Error("Word not found!!!")
            else:
                return Word\
                    .init_form_json(db_record_dict)\
                    .get_pretty_view()

    async def delete_word(self, word):
        try:
            result = await self.db_layer.word.find_one_and_delete(word)
            if result is not None:
                sound_record_path = result['sound_record_path']
                if sound_record_path is not None:
                    remove_file(sound_record_path)
            else:
                return Error("Word not found!!!")
        except Exception as exp:
            return self.__unexpected_exception__(exp)
        else:
            return "Word was deleted!!!"

    async def update_word(self, arg_json):
        try:
            json_dict = validate_json(Word.get_json_schema(), arg_json)
            word = json_dict['word']
            new_json_dict = exclude_json_fields(json_dict, fields=['translation',
                                                                   'phrase',
                                                                   'synonyms'])
            if new_json_dict:
                result = await self.db_layer.word.find_one_and_update(word, new_json_dict)
                if result is None:
                    return Error("Word not found!!!")
        except (TypeError, ValidationError) as exp:
            return Error(exp)
        except JSONDecodeError:
            return Error("Not valid JSON was passed.")
        except Exception as exp:
            return self.__unexpected_exception__(exp)
        else:
            return "Word was updated!!!"

    async def save_word(self, arg_json):
        try:
            word_inst = Word.init_form_json(validate_json(Word.get_json_schema(), arg_json))
            if await self.db_layer.word.record_is_exists(word_inst.word):
                return Error("The dictionary already contains this word. Word - {}".format(word_inst.word))
            await self.db_layer.word.save(vars(word_inst))
            await self.producer.send_message(WordKafkaMessage(word_inst.word))
        except (TypeError, ValidationError) as exp:
            return Error(exp)
        except JSONDecodeError:
            return Error("Not valid JSON was passed.")
        except Exception as exp:
            return self.__unexpected_exception__(exp)
        else:
            return "Word was added!!!"

    def __unexpected_exception__(self, exp):
        self.module_logger.error("Exception : {}".format(exp))
        return Error("Something was wrong")
