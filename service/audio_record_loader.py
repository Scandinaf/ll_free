import asyncio
import os

import aiohttp

from model.http_exception import HttpException

dir_path = "E:\\dictionary\\"

soundoftext_url = "https://api.soundoftext.com/sounds"
soundoftext_request_headers = {'content-type': 'application/json'}
data_template = """{{"engine": "Google", "data": {{"text": "{}", "voice": "en-US"}}}}"""

file_storage_url = "https://soundoftext.nyc3.digitaloceanspaces.com/{}.mp3"
file_storage_request_headers = {'Accept-Encoding': 'gzip, deflate, br',
                        'Host': 'soundoftext.nyc3.digitaloceanspaces.com',
                        'Connection': 'keep-alive'}

chunk_size = 1024


def __build_body__(word):
    return data_template.format(word)


def __get_file_path__(word):
    file_name = __get_file_name__(word) + ".mp3"
    return os.path.join(dir_path, file_name)


def __get_file_name__(word):
    if len(word) > 10:
        return word[:10] + ".{}".format(hash(word))
    else:
        return word


async def __response_bytes_to_file__(file_path, audio_file_response):
    with open(file_path, 'xb') as fd:
        async for data in audio_file_response.content.iter_chunked(chunk_size):
            fd.write(data)


async def __load_file_request__(session, data, word):
    if data["success"]:
        async with session.get(file_storage_url.format(data["id"]),
                               headers=file_storage_request_headers) as audio_file_response:
            await __response_status_handler__(audio_file_response)
            file_path = __get_file_path__(word)
            await __response_bytes_to_file__(file_path, audio_file_response)
            return file_path


async def __load_file_request_retry__(session, data, word, retry_count=3, delay=3):
    try:
        return await __load_file_request__(session, data, word)
    except HttpException as exp:
        if exp.status == 403 and retry_count > 0:
            await asyncio.sleep(delay)
            await __load_file_request_retry__(session, data, word, retry_count=retry_count-1, delay=delay)
        else:
            raise


async def load_audio_record(word):
    word = str(word)
    async with aiohttp.ClientSession() as session:
        async with session.post(soundoftext_url,
                                data=__build_body__(word),
                                headers=soundoftext_request_headers) as response:
            await __response_status_handler__(response)
            return await __load_file_request_retry__(session, await response.json(), word)


async def __response_status_handler__(response):
    if response.status != 200:
        raise HttpException(await response.text(), response.status)
