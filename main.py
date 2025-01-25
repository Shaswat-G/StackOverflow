import json
from answer_analysis import AnswerAnalyzer

def main():
    with open("answer_analysis/db_config.json", "r") as config_file:
        db_config = json.load(config_file)

    analyzer = AnswerAnalyzer(db_config, db_config["collection_name"])
    
    try:
        results = analyzer.analyze(limit=10)  # Analyze 10 answers
        print("Analysis Results:")
        for i, result in enumerate(results, start=1):
            print(f"Answer {i}: {result}")
    finally:
        analyzer.close_connection()

if __name__ == "__main__":
    main()
