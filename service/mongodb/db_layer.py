from service.mongodb.mongodb_word_service import MongoDBWord
from motor.motor_asyncio import AsyncIOMotorClient


class DBLayer:
    def __init__(self, loop, host="localhost", port=27017):
        if loop is None:
            self.client = AsyncIOMotorClient(host, port)
        else:
            self.client = AsyncIOMotorClient(host, port, io_loop=loop)
        self.word = MongoDBWord(mongo_client=self.client)