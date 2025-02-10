import json
from tqdm import tqdm  # added for progress display
from .mongo_connection import MongoDBConnection
from .answer_extractor import AnswerExtractor
from .answer_metrics import AnswerMetrics

class AnswerAnalyzer:
    
    def __init__(self, db_config: dict, collection_name: str, limit: int, results_path: str):
        self.db_config = db_config
        self.collection_name = collection_name
        self.limit = limit
        self.results_path = results_path
        self.db_connection = MongoDBConnection(self.db_config['uri'], self.db_config['database_name'])
        self.db_connection.connect()
        self.answer_extractor = AnswerExtractor(self.db_connection, self.collection_name)
        
    def analyze(self) -> list:
        answer_documents = self.answer_extractor.fetch_and_extract(self.limit)
        print(f"Starting analysis of {len(answer_documents)} documents...")
        results = []
        for answer_document in tqdm(answer_documents, desc="Analyzing answers", unit="doc"):
            question_id = answer_document.get("question_id")
            creation_date = answer_document.get("creation_date")
            metrics = AnswerMetrics(answer_document.get("answers"), creation_date).compute_metrics()
            results.append({
                "question_id": question_id,
                "time_metrics": metrics.get("time_metrics"),
                "per_answer_metrics": metrics.get("per_answer_metrics")
            })
        self.results = results
        print(f"Analysis completed. Processed {len(results)} documents.")
        return results
        
    def save_results(self):
        print(f"Saving results to {self.results_path} ...")
        with open(self.results_path, "w") as out_file:
            json.dump(self.results, out_file, indent=2)
        print("Results saved.")
        
    def close_connection(self):
        self.db_connection.close()
