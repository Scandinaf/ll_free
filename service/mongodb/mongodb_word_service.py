import pymongo
from pymongo import ReturnDocument, UpdateOne

from service.mongodb.mongodb_service import MongoDB
from utils.helper import DateTimeHelper


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
                                      ("last_repeat_date", pymongo.ASCENDING)],
                                     name="Study_status_Last_repeat_date_Index")

    def __get_query_by_word__(self, word):
            return {'word_lower': word.lower()}

    async def get_list_to_study(self, count=10):
        date_helper = DateTimeHelper()
        return await self.collection.find({'$or' : [
            {'study_status' : 6, 'last_repeat_date' : {'$lte' : date_helper.subtract_months(6)}},
            {'study_status': 5, 'last_repeat_date': {'$lte': date_helper.subtract_months(2)}},
            {'study_status': 4, 'last_repeat_date': {'$lte': date_helper.subtract_days(14)}},
            {'study_status': 3, 'last_repeat_date': {'$lte': date_helper.subtract_days(5)}},
            {'study_status': 2, 'last_repeat_date': {'$lte': date_helper.subtract_days(1)}},
            {'study_status': 1, 'last_repeat_date': {'$lte': date_helper.subtract_minutes(30)}},
            {'study_status': 0, 'last_repeat_date': None}
        ]}).sort([("study_status", pymongo.DESCENDING),
                  ("last_repeat_date", pymongo.ASCENDING)])\
            .limit(count).to_list(length=count)

    async def update_study_status(self, word_list):
        helper = DateTimeHelper()
        return await self.collection.bulk_write(list(map(lambda word:
                                                         UpdateOne({'word_lower': word.word_lower},
                                                                   {'$inc': {'study_status': 1},
                                                                    '$set': {'last_repeat_date':
                                                                                 helper.get_current_date_time()}}),
                                                         word_list)))

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
