from getopt import GetoptError

import pytest

from model.word import Word
from service.command_line_arg_parser import CommandLineArgParser


def test_correct_parsing():
    result = CommandLineArgParser(["-a",
                                   "-w", "bad",
                                   "-t", "плохой",
                                   "-p", "Bad dad",
                                   "-s", "poor,bad,bad"])\
        .arg_dict_to_json(Word)
    assert result == """{"word": "bad", "translation": "плохой", "phrase": "Bad dad", "synonyms": ["poor", "bad", "bad"]}"""


def test_not_valid_args():
    result = CommandLineArgParser("-a -w bad").arg_dict
    assert result == {}

    with pytest.raises(TypeError):
        CommandLineArgParser(123)

    with pytest.raises(GetoptError):
        CommandLineArgParser(["-nef"])


def test_valid_args():
    result = CommandLineArgParser(["-a", "-w", "bad"]).arg_dict
    assert result == {"-a": "", "-w": "bad"}
