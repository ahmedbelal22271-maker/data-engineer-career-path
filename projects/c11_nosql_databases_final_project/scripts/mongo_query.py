from pymongo import MongoClient

# Connect to local MongoDB
connecturl = "mongodb://localhost:27017/"

print("Connecting to mongodb server")
connection = MongoClient(connecturl)

# Select the 'training' database
db = connection.training

# Select the 'python' collection
collection = db.python

# Create a sample document
doc = {
    "lab": "Accessing mongodb using python",
    "Subject": "No SQL Databases"
}

# Insert a sample document
print("Inserting a document into collection.")
collection.insert_one(doc)

# Query all documents
docs = collection.find()

print("Printing the documents in the collection.")

for document in docs:
    print(document)

# Close the connection
print("Closing the connection.")
connection.close()
