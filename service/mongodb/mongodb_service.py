class MongoDB:
    def __init__(self, db_name, collection_name, mongo_client):
        self.collection = mongo_client[db_name][collection_name]

    async def save(self, obj):
        return await self.collection.insert_one(obj)
