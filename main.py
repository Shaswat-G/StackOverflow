import json
from answer_analysis import AnswerAnalyzer

def read_config(config_path: str) -> dict:
    print(f"Reading configuration from {config_path} ...")
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    print("Configuration loaded.")
    return config

def main():
    print("Starting main process...")
    config_path = "answer_analysis/db_config.json"
    db_config = read_config(config_path)
    
    analyzer = AnswerAnalyzer(db_config, db_config["collection_name"], limit=10, results_path="results.json")
    analyzer.analyze()
    analyzer.save_results()
    analyzer.close_connection()
    print("Process completed.")

if __name__ == "__main__":
    main()
