import json


class Word:
    def __init__(self, word, translation, phrase=None, synonyms=[],
                 sound_record_path=None, study_status=None,
                 last_repeat_date=None, *args, **keywords):
        self.word = word.strip()
        self.word_lower = self.word.lower()
        self.translation = translation
        self.phrase = phrase.strip() if phrase is not None else None
        self.synonyms = synonyms
        self.sound_record_path = sound_record_path
        self.study_status = study_status
        self.last_repeat_date = last_repeat_date

    def get_pretty_view(self):
        return 'Word - {}\n'.format(self.word) \
               + 'Translation - {}\n'.format(self.translation) \
               + 'Phrase - {}\n'.format(self.phrase) \
               + 'Synonyms - {}\n'.format(','.join(self.synonyms))

    @classmethod
    def init_form_json(cls, json_dic):
        return cls(**json_dic)

    @classmethod
    def get_json_schema(cls):
        return {
            "type": "object",
            "properties": {
                "word": {"type": "string",
                         "maxLength": 40},
                "translation": {"type": "string"},
                "phrase": {"type": "string"},
                "synonyms": {
                    "type": "array",
                    "items":
                        {"type": "string"}
                            }
            },
            "required": ["word"]
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
