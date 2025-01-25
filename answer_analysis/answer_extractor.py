class AnswerExtractor:
    
    def __init__(self, db_connection, collection_name: str):
        self.db_connection = db_connection
        self.collection_name = collection_name
        
    def get_answers(self, limit: int = 100):
        collection = self.db_connection.get_collection(self.collection_name)
        documents = collection.find({}, {"matched_answers":1}).limit(limit)
        return list(documents)
    
    def extract_fields(self, answer: dict):
        relevant_fields = {
            "answer_id": answer.get("_id"),
            "body": answer.get("body", ""),
            "score": answer.get("score", 0),
            "is_accepted": answer.get("is_accepted", False),
            "comment_count": answer.get("comment_count", 0),
            "up_vote_count": answer.get("up_vote_count", 0),
            "down_vote_count": answer.get("down_vote_count", 0)
        }
        return relevant_fields
    
    def fetch_and_extract(self, limit: int = 100):
        answers = self.get_answers(limit)
        all_answers = []
        matched_answers = [answer.get("matched_answers", []) for answer in answers]
        for answer_list in matched_answers:
            for answer in answer_list:
                extracted_answer = self.extract_fields(answer)
                all_answers.append(extracted_answer)
        return all_answers