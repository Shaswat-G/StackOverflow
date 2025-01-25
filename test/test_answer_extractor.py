import unittest
from mongo_connection import MongoDBConnection
from answer_extractor import AnswerExtractor
import json

class TestAnswerExtractor(unittest.TestCase):
    def setUp(self):
        with open ("db_config.json", "r") as config_file:
            self.config = json.load(config_file)
            
        self.db_connection = MongoDBConnection(self.config["uri"], self.config["database_name"])
        self.db_connection.connect()
        
        self.answer_extractor = AnswerExtractor(self.db_connection, self.config["collection_name"])
        
    def test_get_answers(self):
        documents = self.answer_extractor.get_answers(limit=10)
        self.assertGreater(len(documents), 0, "Should fetch at least one document.")
        print("Get answers test passed.")
        
    def test_extract_fields(self):
        sample_answer = {
            "_id": 3144306,
            "body": "<p>Example answer</p>",
            "score": 10,
            "is_accepted": True,
            "comment_count": 2,
            "up_vote_count": 15,
            "down_vote_count": 3
        }
        extracted = self.answer_extractor.extract_fields(sample_answer)
        self.assertEqual(extracted["answer_id"], 3144306)
        self.assertEqual(extracted["score"], 10)
        self.assertTrue(extracted["is_accepted"])
        print("Extract fields test passed.")
        
    def test_fetch_and_extract(self):
        extracted_answers = self.answer_extractor.fetch_and_extract(limit=10)
        self.assertGreater(len(extracted_answers), 0, "Should extract at least one answer.")
        print("Fetch and extract test passed.")
        
    def tearDown(self):
        self.db_connection.close()
        
if __name__ == "__main__":
    unittest.main()
        