class Word:
    sound_record_path = None
    study_status = None
    last_repeat_date = None

    def __init__(self, word, translation, phrase=None, synonyms=[]):
        self.word = word.strip()
        self.translation = translation
        self.phrase = phrase.strip() if phrase is not None else None
        self.synonyms = synonyms

    @classmethod
    def init_form_json(cls, json_dic):
        return cls(**json_dic)

    @classmethod
    def get_json_schema(cls):
        return {
            "type" : "object",
            "properties": {
                "word": {"type" : "string",
                         "maxLength": 40},
                "translation": {"type" : "string"},
                "phrase": {"type": "string"},
                "synonyms": { "type": "array",
                              "items": {"type": "string"}
                             }
            },
            "required": ["word", "translation"]
        }
