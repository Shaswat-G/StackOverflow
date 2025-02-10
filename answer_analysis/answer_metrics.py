import re
import numpy as np
from scipy import stats

class AnswerMetrics:
    def __init__(self, answers: list, question_creation_date: int):
        self.answers = answers
        self.question_creation_date = question_creation_date

    def _word_count(self, answer: dict) -> int:
        body_text = re.sub(r'<[^>]+>', '', answer.get("body", ""))
        return len(re.findall(r'\b\w+\b', body_text))
    
    def _contains_code(self, answer: dict) -> bool:
        body_text = answer.get("body", "")
        return "<code>" in body_text
    
    def _average_word_length(self, answer: dict) -> float:
        body_text = re.sub(r'<[^>]+>', '', answer.get("body", ""))
        words = re.findall(r'\b\w+\b', body_text)
        if not words:
            return 0.0
        return sum(len(word) for word in words) / len(words)
    
    def _engagement_score(self, answer: dict) -> int:
        up_votes = answer.get("up_vote_count", 0)
        down_votes = answer.get("down_vote_count", 0)
        comment_count = answer.get("comment_count", 0)
        return (up_votes - down_votes) + 0.1 * comment_count
    
    def compute_metrics(self, generate_time_metrics: bool = True) -> dict:
        per_answer_metrics = []
        for answer in self.answers:
            complexity = {
                "word_count": self._word_count(answer),
                "contains_code": self._contains_code(answer),
                "average_word_length": self._average_word_length(answer)
            }
            engagement = {
                "engagement_score": self._engagement_score(answer),
                "is_accepted": answer.get("is_accepted", False),
                "score": answer.get("score", 0)
            }
            per_answer_metrics.append({
                "answer_id": answer.get("answer_id"),
                "complexity": complexity,
                "engagement": engagement
            })
        
        if generate_time_metrics:
            time_metrics = compute_time_metrics(self.answers, self.question_creation_date)
        else:
            time_metrics = {}
        
        return {
            "time_metrics": time_metrics,
            "per_answer_metrics": per_answer_metrics
        }

def compute_time_metrics(answers: list, question_creation_date: int) -> dict:
    delays = [(ans.get("creation_date", 0) - question_creation_date) / 3600 for ans in answers if ans.get("creation_date")]
    
    if delays:
        count = len(delays)
        delay_min = np.min(delays)
        delay_max = np.max(delays)
        mean_delay = np.mean(delays)
        median_delay = np.median(delays)
        std_delay = np.std(delays)
        q1, q3 = np.percentile(delays, [25, 75])
        if count > 1:
            skewness = stats.skew(delays)
            kurtosis = stats.kurtosis(delays)
        else:
            skewness = "Undefined"
            kurtosis = "Undefined"
        total_time = delay_max if delay_max > 0 else 1
        answer_rate = count / total_time
        
        return {
            "total_answers": count,
            "min_delay": delay_min,
            "max_delay": delay_max,
            "mean_delay": mean_delay,
            "median_delay": median_delay,
            "std_delay": std_delay,
            "q1": q1,
            "q3": q3,
            "skewness": skewness,
            "kurtosis": kurtosis,
            "answer_rate": answer_rate
        }
    else:
        return {
            "total_answers": 0,
            "min_delay": None,
            "max_delay": None,
            "mean_delay": None,
            "median_delay": None,
            "std_delay": None,
            "q1": None,
            "q3": None,
            "skewness": None,
            "kurtosis": None,
            "answer_rate": None
        }