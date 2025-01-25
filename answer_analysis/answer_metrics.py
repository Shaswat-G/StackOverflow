import re

class AnswerMetrics:
    def __init__(self, answer: dict):
        self.answer = answer
        
    def _word_count(self) -> int:
        body_text = re.sub(r'<[^>]+>', '', self.answer.get("body", ""))  # Remove HTML tags
        return len(re.findall(r'\b\w+\b', body_text))
    
    def _contains_code(self) -> bool:
        body_text = self.answer.get("body", "")
        contains_code = "<code>" in body_text
        return contains_code
    
    def _average_word_length(self) -> float:
        body_text = re.sub(r'<[^>]+>', '', self.answer.get("body", ""))
        words = re.findall(r'\b\w+\b', body_text)
        if not words:
            return 0.0
        total_length = sum(len(word) for word in words)
        average_length = total_length / len(words)
        return average_length
    
    def _engagement_score(self) -> int:
        up_votes = self.answer.get("up_vote_count", 0)
        down_votes = self.answer.get("down_vote_count", 0)
        comment_count = self.answer.get("comment_count", 0)
        engagement_score = (up_votes- down_votes) + 0.1 * comment_count
        return engagement_score
    
    def compute_metrics(self) -> dict:
        metrics = {
            "word_count": self._word_count(),
            "contains_code": self._contains_code(),
            "average_word_length": self._average_word_length(),
            "engagement_score": self._engagement_score(),
            "is_accepted": self.answer.get("is_accepted", False),
            "score": self.answer.get("score", 0)
        }
        return metrics