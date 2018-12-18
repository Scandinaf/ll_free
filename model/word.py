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
