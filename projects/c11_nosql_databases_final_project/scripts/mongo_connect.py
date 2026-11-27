from pymongo import MongoClient

# 1. Connection URL (Simple localhost, no auth parameters)
connecturl = "mongodb://localhost:27017/"

# 2. Connect to MongoDB server
print("Connecting to mongodb server")
connection = MongoClient(connecturl)

# 3. Get database list
print("Getting list of databases")
dbs = connection.list_database_names()

# 4. Print the database names
for db in dbs:
    print(db)

# 5. Close connection
print("Closing the connection to the mongodb server")
connection.close()
