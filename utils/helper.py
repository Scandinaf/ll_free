import json
import os
from jsonschema import validate


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def exclude_json_fields(json_dict, fields=[]):
    new_json_dict = {}
    for field in fields:
        if field in json_dict:
            new_json_dict[field] = json_dict[field]
    return new_json_dict


def validate_json(json_schema, arg_json):
    json_dict = json.loads(arg_json)
    validate(json_schema, json_dict)
    return json_dict
