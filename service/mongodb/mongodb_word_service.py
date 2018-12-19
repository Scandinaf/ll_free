import pymongo

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
                                     name = "Study_status_Last_repeat_date_Index")

    async def find_one_by_word(self, word):
        return await self.collection.find_one({'word_lower': word.lower()})
