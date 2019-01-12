import datetime
import json
import os


from jsonschema import validate
import monthdelta


def file_exists(file_path):
    return os.path.exists(file_path)


def remove_file(file_path):
    if file_exists(file_path):
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


def check_index_valid(index, size):
    return not (index < 0 or index >= size)


class DateTimeHelper:
    def __init__(self):
        self.current_date_time = datetime.datetime.utcnow()

    def get_current_date_time(self):
        return self.current_date_time

    def subtract_months(self, months):
        return self.current_date_time - monthdelta.MonthDelta(months=months)

    def subtract_days(self, days):
        return self.current_date_time - datetime.timedelta(days=days)

    def subtract_minutes(self, minutes):
        return self.current_date_time - datetime.timedelta(minutes=minutes)
