import json
from json import JSONDecodeError

from jsonschema import ValidationError

from model.error import Error
from model.word import Word

from service.json_validator import validate_json


def save_word(arg_json):
    try:
        json_dict = json.loads(arg_json)
        validate_json(Word.get_json_schema(), json_dict)
        word = Word.init_form_json(json_dict)
        return "Word was added!!!"
    except (TypeError, ValidationError) as exp:
        return Error(exp)
    except JSONDecodeError:
        return Error("Not valid JSON was passed.")
