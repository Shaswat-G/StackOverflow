class AnswerExtractor:
    
    def __init__(self, db_connection, collection_name: str):
        self.db_connection = db_connection
        self.collection_name = collection_name
        
    def get_answers(self, limit: int = 100):
        collection = self.db_connection.get_collection(self.collection_name)
        documents = list(collection.find({}, {"matched_answers": 1, "creation_date": 1}).limit(limit))
        return documents  # now returning full documents
    
    def extract_fields(self, answer: dict):
        relevant_fields = {
            "answer_id": answer.get("_id"),
            "body": answer.get("body", ""),
            "score": answer.get("score", 0),
            "is_accepted": answer.get("is_accepted", False),
            "comment_count": answer.get("comment_count", 0),
            "up_vote_count": answer.get("up_vote_count", 0),
            "down_vote_count": answer.get("down_vote_count", 0),
            "creation_date": answer.get("creation_date", 0)  # new field for time metrics
        }
        return relevant_fields
    
    def fetch_and_extract(self, limit: int = 100):
        documents = self.get_answers(limit)
        answer_documents = []
        for document in documents:
            answers_per_question = document.get("matched_answers", [])
            creation_date = document.get("creation_date", 0)
            question_id = answers_per_question[0].get("question_id") if answers_per_question else None
            extracted_answers_per_question = []
            for unextracted_answer in answers_per_question:
                extracted_answer = self.extract_fields(unextracted_answer)
                extracted_answers_per_question.append(extracted_answer)
            answer_documents.append({
                "question_id": question_id,
                "answers": extracted_answers_per_question,
                "creation_date": creation_date
            })
        return answer_documents