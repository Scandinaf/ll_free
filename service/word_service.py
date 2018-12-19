import json
import logging
from json import JSONDecodeError

from jsonschema import ValidationError

from model.error import Error
from model.word import Word
from service.json_validator import validate_json


class WordService:
    def __init__(self, db_layer):
        self.db_layer = db_layer
        self.module_logger = logging.getLogger()

    async def get_word(self, word):
        try:
            db_record_dict = await self.db_layer.word.find_one_by_word(word)
        except Exception as exp:
            self.__unexpected_exception__(exp)
        else:
            if db_record_dict is None:
                return Error("Word not found!!!")
            else:
                return Word\
                    .init_form_json(db_record_dict)\
                    .get_pretty_view()

    async def delete_word(self, word):
        try:
            await self.db_layer.word.delete_by_word(word)
        except Exception as exp:
            self.__unexpected_exception__(exp)
        else:
            return "Word was deleted!!!"

    async def save_word(self, arg_json):
        try:
            json_dict = json.loads(arg_json)
            validate_json(Word.get_json_schema(), json_dict)
            word_inst = Word.init_form_json(json_dict)
            if await self.db_layer.word.record_is_exists(word_inst.word):
                return Error("The dictionary already contains this word. Word - {}".format(word_inst.word))
            await self.db_layer.word.save(vars(word_inst))
        except (TypeError, ValidationError) as exp:
            return Error(exp)
        except JSONDecodeError:
            return Error("Not valid JSON was passed.")
        except Exception as exp:
            self.__unexpected_exception__(exp)
        else:
            return "Word was added!!!"

    def __unexpected_exception__(self, exp):
        self.module_logger.error("Exception : {}".format(exp))
        return Error("Something was wrong")
