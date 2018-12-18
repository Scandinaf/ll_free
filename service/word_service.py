import json
import logging
from json import JSONDecodeError

from jsonschema import ValidationError

from model.error import Error
from model.http_exception import HttpException
from model.word import Word
from service.audio_record_loader import AudioRecordLoader
from service.json_validator import validate_json

audio_loader_service = AudioRecordLoader(dir_path = "E:\\dictionary\\")
module_logger = logging.getLogger()


async def save_word(arg_json):
    try:
        json_dict = json.loads(arg_json)
        validate_json(Word.get_json_schema(), json_dict)
        word_inst = Word.init_form_json(json_dict)
        await __init_audio_record_path__(word_inst)
        return "Word was added!!!"
    except (TypeError, ValidationError) as exp:
        return Error(exp)
    except JSONDecodeError:
        return Error("Not valid JSON was passed.")
    except Exception as exp:
        module_logger.error("Exception : {}".format(exp))
        return Error("Something was wrong")


async def __init_audio_record_path__(word_inst):
    try:
        word_inst.sound_record_path = await audio_loader_service.load_audio_record(word_inst.word)
    except (FileExistsError, HttpException) as exp:
        module_logger.warning("Error loading file. Exception : {}".format(exp))

