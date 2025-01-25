import json
import unittest
from mongo_connection import MongoDBConnection

class TestMongoDBConnection(unittest.TestCase):
    def setUp(self):
        with open("db_config.json") as file:
            self.config = json.load(file)
        self.mongo = MongoDBConnection(self.config["uri"], self.config["database_name"])
        
    def test_connection(self):
        self.mongo.connect()
        self.assertIsNotNone(self.mongo.db, "Database connection should not be None.")
        print("Connection test passed.")

    def test_get_collection(self):
        self.mongo.connect()
        collection = self.mongo.get_collection(self.config["collection_name"])
        self.assertIsNotNone(collection, "Collection should not be None.")
        print("Get Collection test passed.")
        
    def tearDown(self):
        self.mongo.close()
        
if __name__ == "__main__":
    unittest.main()