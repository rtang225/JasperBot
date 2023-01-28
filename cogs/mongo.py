from discord.ext import commands
from pymongo import MongoClient
from BotConfig import BotConfig

connection = MongoClient(BotConfig.db())
db = connection["Jasper"]

class mongo(commands.Cog):

    def __init__(self, client):
        self.client = client

#Adding a value (CAN DELETE)
    def insert(self, collection, id, field, *, value):
        collection.insert_one({"_id": id, field: value})

#Read a value
    def get(self, collection, id, field):
        query = collection.find({"_id": id})
        for x in query:
            value = x[field]
        return value

#Edit a value
    def update(self, collection, id, field, *, value):
        collection.update_one({"_id": id}, {"$set": {field: value}})

#Edit by increment
    def increment(self, collection, id, field, increment: int):
        query = collection.find({"_id": id})
        for x in query:
            value = int(x[field])
        value += increment
        collection.update_one({"_id": id}, {"$set": {field: value}})

#Delete an id
    def delete_id(self, collection, id):
        collection.delete_one({"_id": id})

#Delete a field
    def delete_field(self, collection, id, field):
        collection.update_one({"_id": id}, {"$unset":{field: None}})

#Set a field to None
    def zero_field(self, collection, id, field):
        collection.update_one({"_id": id}, {"$set":{field: None}})

async def setup(client):
    await client.add_cog(mongo(client))