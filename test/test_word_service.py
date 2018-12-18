import pytest

from service.word_service import *


@pytest.mark.asyncio
async def test_not_valid_type():
    result = await save_word(123)
    assert isinstance(result, Error)

    result = await save_word(1.0234)
    assert isinstance(result, Error)

    result = await save_word("test")
    assert isinstance(result, Error)

    result = await save_word([])
    assert isinstance(result, Error)


@pytest.mark.asyncio
async def test_not_valid_json():
    result = await save_word("{}")
    assert isinstance(result, Error)

    result = await save_word("""{"word" : "Anyone who reads Old and Middle English literary texts"}""")
    assert isinstance(result, Error)

    result = await save_word("""{"word" : 123}""")
    assert isinstance(result, Error)

    result = await save_word("""{"synonyms" : 123}""")
    assert isinstance(result, Error)

    result = await save_word("""{"synonyms" : [1,2,3]}""")
    assert isinstance(result, Error)


@pytest.mark.asyncio
async def test_required_fields():
    result = await save_word("""{"word": "bad"}""")
    assert isinstance(result, Error)

    result = await save_word("""{"translation": "плохой"}""")
    assert isinstance(result, Error)


@pytest.mark.asyncio
async def test_valid_json(mocker):
    mocker.patch.object(audio_loader_service, 'load_audio_record')
    audio_loader_service.load_audio_record.return_value = __default_coroutine__()
    result = await save_word("""{"word" : "bad", "translation": "плохой"}""")
    assert result == "Word was added!!!"


async def __default_coroutine__():
    return None
