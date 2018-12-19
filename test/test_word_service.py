import pytest
from mock import MagicMock

from service.word_service import *


async def __default_coroutine__():
    return None


def __mock_objects__():
    word_service.db_layer = MagicMock()
    word_service.db_layer.word.save.return_value = __default_coroutine__()
    word_service.audio_loader_service = MagicMock()
    word_service.audio_loader_service.load_audio_record.return_value = __default_coroutine__()


word_service = WordService(db_layer=None)
__mock_objects__()


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

    result = await word_service.save_word("""{"word" : "Anyone who reads Old and Middle English literary texts"}""")
    assert isinstance(result, Error)

    result = await word_service.save_word("""{"word" : 123}""")
    assert isinstance(result, Error)

    result = await word_service.save_word("""{"synonyms" : 123}""")
    assert isinstance(result, Error)

    result = await word_service.save_word("""{"synonyms" : [1,2,3]}""")
    assert isinstance(result, Error)


@pytest.mark.asyncio
async def test_required_fields():
    result = await word_service.save_word("""{"word": "bad"}""")
    assert isinstance(result, Error)

    result = await word_service.save_word("""{"translation": "плохой"}""")
    assert isinstance(result, Error)


@pytest.mark.asyncio
async def test_valid_json():
    result = await word_service.save_word("""{"word" : "bad", "translation": "плохой"}""")
    assert result == "Word was added!!!"
