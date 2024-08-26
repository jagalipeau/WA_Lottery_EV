import pymongo
import json

# Connect to MongoDB


def update(new_data, collectionName="full_data"):
    """
    Inserts or updates data in a specified MongoDB collection.

    Args:
        new_data (list): A list of dictionaries containing data to be inserted or updated.
        collectionName (str, optional): The name of the MongoDB collection. Defaults to "full_data".

    Returns:
        None
    """

    # Connect to MongoDB using pymongo library
    client = pymongo.MongoClient("mongodb://mongoadmin:pass@localhost:27017/")

    # Specify database and collection
    database = client["Wa_Lotto"]
    collection = database[collectionName]

    try:
        # Insert data into specified collection
        collection.insert_many(new_data)
        print("Data inserted successfully.")
    except Exception as e:
        # Handle any exceptions that occur during insertion
        print(f"Failed to insert data: {str(e)}")
    return None


# Define a function to read raw data from the MongoDB collection
def read_raw():
    """
    Retrieves all documents from the 'full_data' MongoDB collection.

    Returns:
        list: A list of dictionaries, where each dictionary represents a document in the collection.
    """

    # Connect to MongoDB using pymongo library
    client = pymongo.MongoClient("mongodb://mongoadmin:pass@localhost:27017/")

    # Specify database and collection
    database = client["Wa_Lotto"]
    collection = database["full_data"]

    # Use find() method to retrieve all documents from the collection
    documents = list(collection.find())

    return documents


# Call the update function with the fake car data
# update(database, main.get_data())
