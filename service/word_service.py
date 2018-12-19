import json
import logging
from json import JSONDecodeError

from jsonschema import ValidationError

from model.error import Error
from model.http_exception import HttpException
from model.word import Word
from service.audio_record_loader import AudioRecordLoader
from service.json_validator import validate_json


class WordService:
    def __init__(self, db_layer):
        self.audio_loader_service = AudioRecordLoader(dir_path="E:\\dictionary\\")
        self.db_layer = db_layer
        self.module_logger = logging.getLogger()

    async def save_word(self, arg_json):
        try:
            json_dict = json.loads(arg_json)
            validate_json(Word.get_json_schema(), json_dict)
            word_inst = Word.init_form_json(json_dict)
            db_record = await self.db_layer.word.find_one_by_word(word_inst.word)
            if db_record is not None:
                return Error("The dictionary already contains this word. Word - {}".format(word_inst.word))
            await self.__init_audio_record_path__(word_inst)
            await self.db_layer.word.save(vars(word_inst))
            return "Word was added!!!"
        except (TypeError, ValidationError) as exp:
            return Error(exp)
        except JSONDecodeError:
            return Error("Not valid JSON was passed.")
        except Exception as exp:
            self.module_logger.error("Exception : {}".format(exp))
            return Error("Something was wrong")

    async def __init_audio_record_path__(self, word_inst):
        try:
            word_inst.sound_record_path = await self.audio_loader_service.load_audio_record(word_inst.word)
        except (FileExistsError, HttpException) as exp:
            self.module_logger.warning("Error loading file. Exception : {}".format(exp))
