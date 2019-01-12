import pytest

from service.audio_record_loader import *

service = AudioRecordLoader(dir_path = "E:\\dictionary_test\\")
invalid_text = """As its name states, EETS was begun as a 'club',
and it retains certain features of that even now. It has no physical location,
or even office, no paid staff or editors, but books in the Original Series are published
in the first place to satisfy subscriptions paid by individuals or institutions.
This means that there is need for a regular sequence of new editions, normally one or two
per year; achieving that sequence can pose problems for the Editorial Secretary,
who may have too few or too many texts ready for publication at any one time.
Details on a separate sheet explain how individual (but not institutional) members can choose
to take certain back volumes in place of the newly published volumes against their subscriptions.
On the same sheet are given details about the very advantageous discount available to individual
members on all back numbers. In 1970 a Supplementary Series was begun, a series which only appears
occasionally (it currently has 24 volumes within it); some of these are new editions of texts earlier
appearing in the main series. Again these volumes are available at publication and later at a substantial
discount to members. All these advantages can only be obtained through the Membership Secretary
(the books are sent by post); they are not available through bookshops, and such bookstores as carry EETS
books have only a very limited selection of the many published."""


@pytest.mark.asyncio
async def test_correct_behaviour():
    file_path = await service.load_audio_record("bad")
    assert "bad.mp3" == file_path[-7:]
    __delete_file__(file_path)

    file_path = await service.load_audio_record(123.323)
    assert "123.323.mp3" == file_path[-11:]
    __delete_file__(file_path)


@pytest.mark.asyncio
async def test_duplicate():
    file_path = await service.load_audio_record("bad")
    assert "bad.mp3" == file_path[-7:]

    with pytest.raises(FileExistsError):
        await service.load_audio_record("bad")
    __delete_file__(file_path)


@pytest.mark.asyncio
async def test_invalid_text():
    with pytest.raises(HttpException):
        await service.load_audio_record(invalid_text)


def __delete_file__(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
