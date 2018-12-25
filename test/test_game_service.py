import pytest
from mock import MagicMock

from model.word import Word
from service.game_service import GameService


async def __default_coroutine__(value=None):
    return value


def __mock_objects__():
    game_service.db_layer = MagicMock()


game_service = GameService(db_layer=None)
__mock_objects__()


@pytest.mark.asyncio
async def test_game_service_words_not_found():
    game_service.db_layer.word.get_list_to_study.return_value = __default_coroutine__([])
    result = await game_service.start_game()
    assert result == "Add new words to the dictionary and come back!!!"


def test_convert_to_inst():
    result = game_service.__convert_to_inst__([{"word": "bad", "translation": "плохой"},
                                               {"word": "bad", "translation": "плохой"},
                                               {"word": "bad", "translation": "плохой"}])
    assert len(result) == 3
    assert result[0].word == "bad"


def test_game_iter_correct():
    bulk_update_dict = {}
    new_index, result = game_service.__game_iter__(1, -1, [Word(word="bad")], bulk_update_dict)
    assert new_index == 0
    assert len(bulk_update_dict) == 1


def test_game_iter_bad_index():
    bulk_update_dict = {}
    new_index, result = game_service.__game_iter__(1, -2, [Word(word="bad")], bulk_update_dict)
    assert new_index == 1
    assert len(bulk_update_dict) == 0
    assert result == "You are trying to go beyond the index."


def test_game_iter_bad_list():
    bulk_update_dict = {}
    with pytest.raises(AttributeError):
        _, _ = game_service.__game_iter__(1, -1, [1,2,3,4], bulk_update_dict)
