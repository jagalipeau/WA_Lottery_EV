import pymongo
import json

# Connect to MongoDB


def update(new_data, collectionName="full_data"):
    client = pymongo.MongoClient("mongodb://mongoadmin:pass@localhost:27017/")

    database = client["Wa_Lotto"]

    collection = database[collectionName]
    try:
        collection.insert_many(new_data)
        print("successful")
    except:
        print("failed")

    return None


def read_raw():
    # Gets all documents from the full_data collection
    client = pymongo.MongoClient("mongodb://mongoadmin:pass@localhost:27017/")

    database = client["Wa_Lotto"]

    collection = database["full_data"]

    documents = list(collection.find())

    return documents


# Call the update function with the fake car data
# update(database, main.get_data())
read_raw()
