import pymongo
from pymongo import ReturnDocument

from service.mongodb.mongodb_service import MongoDB


class MongoDBWord(MongoDB):
    db_name = "project"
    collection_name = "dictionary"

    def __init__(self, mongo_client):
        MongoDB.__init__(self, self.db_name, self.collection_name, mongo_client)
        self.__init_indexes__()

    def __init_indexes__(self):
        self.collection.create_index([("word", pymongo.ASCENDING)],
                                     unique=True,
                                     name="Word_Unique_Index")
        self.collection.create_index([("study_status", pymongo.DESCENDING),
                                      ("last_repeat_date", pymongo.DESCENDING)],
                                     name="Study_status_Last_repeat_date_Index")

    def __get_query_by_word__(self, word):
            return {'word_lower': word.lower()}

    async def find_one_by_word(self, word):
        return await self.collection.find_one(self.__get_query_by_word__(word))

    async def find_one_and_update(self, word, json_dict):
        return await self.collection.find_one_and_update(self.__get_query_by_word__(word),
                                                         {"$set": json_dict},
                                                         return_document=ReturnDocument.AFTER)

    async def record_is_exists(self, word):
        db_record_dict = await self.collection.find_one(
            self.__get_query_by_word__(word))
        return db_record_dict is not None

    async def find_one_and_delete(self, word):
        return await self.collection.find_one_and_delete(
            self.__get_query_by_word__(word))

    async def update_audio_record_path(self, word, sound_record_path):
        return await self.collection.update_one(self.__get_query_by_word__(word),
                                                {"$set": {'sound_record_path' : sound_record_path}})
