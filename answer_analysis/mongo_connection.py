from pymongo import MongoClient

class MongoDBConnection:
    def __init__(self, uri: str, database_name: str):
        self.uri = uri
        self.database_name = database_name
        self.client = None
        self.db = None
        
    def connect(self):
        self.client = MongoClient(self.uri)
        self.db = self.client[self.database_name]
        print(f"[INFO] Connected to MongoDB : {self.database_name}")
        
    def get_collection(self, collection_name: str):
        if self.db is None:
            raise ConnectionError("Database connection is not established. Call connect() first.")
        return self.db[collection_name]
    
    def close(self):
        if self.client:
            self.client.close()
            print("[INFO] Connection to MongoDB is closed.")
