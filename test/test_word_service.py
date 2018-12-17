import unittest
from service.word_service import *


class TestWordService(unittest.TestCase):
    def test_not_valid_type(self):
        self.assertIsInstance(save_word(123), Error)
        self.assertIsInstance(save_word(1.0234), Error)
        self.assertIsInstance(save_word("test"), Error)
        self.assertIsInstance(save_word([]), Error)

    def test_not_valid_json(self):
        self.assertIsInstance(save_word("{}"), Error)
        self.assertIsInstance(save_word("""{"word" : "Anyone who reads Old and Middle English literary texts"}"""),
                              Error)
        self.assertIsInstance(save_word("""{"word" : 123}"""), Error)
        self.assertIsInstance(save_word("""{"synonyms" : 123}"""), Error)
        self.assertIsInstance(save_word("""{"synonyms" : [1,2,3]}"""), Error)

    def test_required_fields(self):
        self.assertIsInstance(save_word("""{"word": "bad"}"""), Error)
        self.assertIsInstance(save_word("""{"translation": "плохой"}"""), Error)

    def test_valid_json(self):
        self.assertEqual(save_word("""{"word" : "bad", "translation": "плохой"}"""), "Word was added!!!")
