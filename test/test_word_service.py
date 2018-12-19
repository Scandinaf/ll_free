import pytest

from service.word_service import *

word_service = WordService(db_layer=None)


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
async def test_valid_json(mocker):
    mocker.patch.object(word_service.audio_loader_service, 'load_audio_record')
    word_service.audio_loader_service.load_audio_record.return_value = __default_coroutine__()
    mocker.patch.object(word_service.db_layer.word, 'save')
    word_service.db_layer.word.save.return_value = __default_coroutine__()
    result = await word_service.save_word("""{"word" : "bad", "translation": "плохой"}""")
    assert result == "Word was added!!!"


async def __default_coroutine__():
    return None
