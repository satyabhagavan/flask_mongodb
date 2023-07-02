## script to load the data to mongoDb
import json
from pymongo import MongoClient

# Establish a connection to MongoDB
client = MongoClient('add the mongodb uri')

# Select the database
db = client['information']

# Select the collection
collection = db['data']


# Read the JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

# Insert the data into the collection
collection.insert_many(data)

# Close the MongoDB connection
client.close()
