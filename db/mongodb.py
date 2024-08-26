import pymongo


class MongoDB:
    def __init__(self, url, database_name):
        self.client = pymongo.MongoClient(url)
        self.db = self.client[database_name]

    def insert(self, collection_name, document):
        self.db[collection_name].insert_one(document)

    def insert_many(self, collection_name, document_list):
        self.db[collection_name].insert_many(document_list)

    def find(self, collection_name, query=None):
        return self.db[collection_name].find(query)

    def update(self, collection_name, query, update):
        self.db[collection_name].update_one(query, update)

    def delete(self, collection_name, query):
        self.db[collection_name].delete_one(query)

      