import pytest
from mock import MagicMock

from service.word_service import *


async def __default_coroutine__(value=None):
    return value


def __mock_objects__():
    word_service.db_layer = MagicMock()
    word_service.db_layer.word.save.return_value = __default_coroutine__()
    word_service.producer = MagicMock()
    word_service.producer.send_message.return_value = __default_coroutine__()


word_service = WordService(db_layer=None, producer=None)
__mock_objects__()


@pytest.mark.asyncio
async def test_update_word_correct():
    word_service.db_layer.word.find_one_and_update.return_value = __default_coroutine__({"word": "bad"})
    result = await word_service.update_word("""{"word" : "bad", "translation": "плохой"}""")
    assert result == "Word was updated!!!"


@pytest.mark.asyncio
async def test_update_word_invalid_json():
    result = await word_service.update_word("""{"translation": "плохой"}""")
    assert isinstance(result, Error)

    result = await word_service.update_word("""{"word_new": "bad"}""")
    assert isinstance(result, Error)

    result = await word_service.update_word([])
    assert isinstance(result, Error)

    result = await word_service.update_word(123)
    assert isinstance(result, Error)

    result = await word_service.update_word("just text")
    assert isinstance(result, Error)


@pytest.mark.asyncio
async def test_update_word_not_found():
    word_service.db_layer.word.find_one_and_update.return_value = __default_coroutine__()
    result = await word_service.update_word("""{"word" : "bad", "translation": "плохой"}""")
    assert isinstance(result, Error)


@pytest.mark.asyncio
async def test_get_word_not_found():
    word_service.db_layer.word.find_one_by_word.return_value = __default_coroutine__()
    result = await word_service.get_word("test")
    assert isinstance(result, Error)


@pytest.mark.asyncio
async def test_get_word_correct():
    word_dict = {'word': 'bad', 'translation': 'плохой', 'synonyms': ["poor", "bad"]}
    word_service.db_layer.word.find_one_by_word.return_value = __default_coroutine__(word_dict)
    result = await word_service.get_word("test")
    assert isinstance(result, str)


@pytest.mark.asyncio
async def test_delete_word_not_found():
    word_service.db_layer.word.find_one_and_delete.return_value = __default_coroutine__()
    result = await word_service.delete_word("test")
    assert isinstance(result, Error)


@pytest.mark.asyncio
async def test_delete_word_correct():
    word_service.db_layer.word.find_one_and_delete.return_value = \
        __default_coroutine__({"sound_record_path" : None})
    result = await word_service.delete_word("test")
    assert result == "Word was deleted!!!"


@pytest.mark.asyncio
async def test_not_valid_type():
    result = await word_service.save_word(123)
    assert isinstance(result, Error)

    result = await word_service.save_word(1.0234)
    assert isinstance(result, Error)

    result = await word_service.save_word("test")
    assert isinstance(result, Error)

    result = await word_service.save_word([])
    assert isinstance(result, Error)


@pytest.mark.asyncio
async def test_not_valid_json():
    result = await word_service.save_word("{}")
    assert isinstance(result, Error)

    result = await word_service.save_word("""{"translation" : "Anyone who reads Old and Middle English literary texts"}""")
    assert isinstance(result, Error)

    result = await word_service.save_word("""{"word" : 123}""")
    assert isinstance(result, Error)

    result = await word_service.save_word("""{"synonyms" : 123}""")
    assert isinstance(result, Error)

    result = await word_service.save_word("""{"synonyms" : [1,2,3]}""")
    assert isinstance(result, Error)

    word_service.db_layer.word.record_is_exists.return_value = __default_coroutine__(True)
    result = await word_service.save_word("""{"word" : "bad", "translation": "плохой"}""")
    assert isinstance(result, Error)


@pytest.mark.asyncio
async def test_required_fields():
    result = await word_service.save_word("""{"word": "bad"}""")
    assert isinstance(result, Error)

    result = await word_service.save_word("""{"translation": "плохой"}""")
    assert isinstance(result, Error)


@pytest.mark.asyncio
async def test_valid_json():
    word_service.db_layer.word.record_is_exists.return_value = __default_coroutine__(False)
    result = await word_service.save_word("""{"word" : "bad", "translation": "плохой"}""")
    assert result == "Word was added!!!"
