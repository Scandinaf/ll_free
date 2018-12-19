import json


class Word:
    def __init__(self, word, translation, phrase=None, synonyms=[]):
        self.word = word.strip()
        self.translation = translation
        self.phrase = phrase.strip() if phrase is not None else None
        self.synonyms = synonyms
        self.sound_record_path = None
        self.study_status = None
        self.last_repeat_date = None

    @classmethod
    def init_form_json(cls, json_dic):
        return cls(**json_dic)

    @classmethod
    def get_json_schema(cls):
        return {
            "type": "object",
            "properties": {
                "word": {"type" : "string",
                         "maxLength": 40},
                "translation": {"type": "string"},
                "phrase": {"type": "string"},
                "synonyms": {
                    "type": "array",
                    "items":
                        {"type": "string"}
                            }
            },
            "required": ["word", "translation"]
        }

    @classmethod
    def arg_dict_to_json(cls, arg_dict):
        def __arg_to_key__(arg_name, key_name):
            if arg_name in arg_dict:
                json_dict[key_name] = arg_dict[arg_name]
        json_dict = {}
        __arg_to_key__('-w', 'word')
        __arg_to_key__('-t', 'translation')
        __arg_to_key__('-p', 'phrase')
        if '-s' in arg_dict:
            json_dict['synonyms'] = arg_dict['-s'].split(",")
        return json.dumps(json_dict, ensure_ascii=False)
