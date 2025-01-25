import unittest
from answer_metrics import AnswerMetrics

class TestAnswerMetrics(unittest.TestCase):
    def setUp(self):
        self.sample_answer = {
            "body": "<p>This is a sample answer with some code:</p><code>print('Hello')</code>",
            "score": 10,
            "is_accepted": True,
            "comment_count": 3,
            "up_vote_count": 15,
            "down_vote_count": 2
        }
        self.metrics = AnswerMetrics(self.sample_answer)
        
    def test_word_count(self):
        self.assertEqual(self.metrics._word_count(), 10, "Word count should be 10.")

    def test_contains_code(self):
        self.assertTrue(self.metrics._contains_code(), "Answer should contain code.")

    def test_average_word_length(self):
        self.assertAlmostEqual(self.metrics._average_word_length(), 4.1, places=1, msg="Average word length should be approximately 4.5.")

    def test_engagement_score(self):
        self.assertEqual(self.metrics._engagement_score(), 13.3, "Engagement score should be 16.")

    def test_compute_metrics(self):
        computed_metrics = self.metrics.compute_metrics()
        self.assertEqual(computed_metrics["word_count"], 10)
        self.assertTrue(computed_metrics["contains_code"])
        self.assertAlmostEqual(computed_metrics["average_word_length"], 4.1, places=1)
        self.assertEqual(computed_metrics["engagement_score"], 13.3)
        self.assertTrue(computed_metrics["is_accepted"])
        self.assertEqual(computed_metrics["score"], 10)

if __name__ == "__main__":
    unittest.main()