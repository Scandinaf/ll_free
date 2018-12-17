from jsonschema import validate


def validate_json(schema, json):
    validate(json, schema)