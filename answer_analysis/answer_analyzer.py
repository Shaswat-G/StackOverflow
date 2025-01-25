from .mongo_connection import MongoDBConnection
from .answer_extractor import AnswerExtractor
from .answer_metrics import AnswerMetrics

class AnswerAnalyzer:
    
    def __init__(self, db_config: dict, collection_name: str):
        self.db_config = db_config
        self.collection_name = collection_name
        self.db_connection = MongoDBConnection(self.db_config['uri'], self.db_config['database_name'])
        self.db_connection.connect()
        self.answer_extractor = AnswerExtractor(self.db_connection, self.collection_name)
        
    def analyze(self, limit: int = 100) -> list:
        
        extracted_answers = self.answer_extractor.fetch_and_extract(limit)
        
        results = []
        for answer in extracted_answers:
            metrics = AnswerMetrics(answer).compute_metrics()
            results.append(metrics)

        return results
        
    def close_connection(self):
        self.db_connection.close()
