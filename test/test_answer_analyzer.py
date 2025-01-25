import unittest
import json
from answer_analyzer import AnswerAnalyzer

class TestAnswerAnalyzer(unittest.TestCase):
    def setUp(self):
        with open("db_config.json") as file:
            self.db_config = json.load(file)
        self.collection_name = self.db_config["collection_name"]
        self.analyzer = AnswerAnalyzer(self.db_config, self.collection_name)
        
    def test_analyze(self):
        results = self.analyzer.analyze(limit=5)
        self.assertGreater(len(results), 0, "Results should not be empty.")
        for result in results:
            self.assertIn("word_count", result)
            self.assertIn("contains_code", result)
            self.assertIn("engagement_score", result)
        print("Analyze test passed.")

    def tearDown(self):
        self.analyzer.close_connection()

if __name__ == "__main__":
    unittest.main()