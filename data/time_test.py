import json
import numpy as np
from datetime import datetime, timezone
from scipy import stats  # new import

# Load JSON file
with open("sample_document.json", "r") as f:
    data = json.load(f)

# Extract question creation timestamp & convert to datetime
question_time = datetime.fromtimestamp(data["creation_date"], tz=timezone.utc)

# Extract answer timestamps and compute delays (in hours) relative to question posting
answer_times = [datetime.fromtimestamp(ts, tz=timezone.utc) for ts in [a["creation_date"] for a in data.get("answers", [])]]
delays = [(ans_time - question_time).total_seconds() / 3600 for ans_time in answer_times]

# Compute basic metrics if answers exist
if delays:
    count = len(delays)
    delay_min = np.min(delays)
    delay_max = np.max(delays)
    mean_delay = np.mean(delays)
    median_delay = np.median(delays)
    std_delay = np.std(delays)
    q1, q3 = np.percentile(delays, [25, 75])
    skewness = stats.skew(delays)
    kurtosis = stats.kurtosis(delays)

    # Calculate answer rate: answers per hour over the full elapsed period until the last answer
    total_time = delay_max if delay_max > 0 else 1  # avoid division by zero
    answer_rate = count / total_time

    # Display Results
    print(f"Total answers: {count}")
    print(f"Delay (hours)  -> min: {delay_min:.2f}, max: {delay_max:.2f}, mean: {mean_delay:.2f}, median: {median_delay:.2f}")
    print(f"Standard Deviation: {std_delay:.2f}")
    print(f"25th percentile: {q1:.2f}, 75th percentile: {q3:.2f}")
    print(f"Skewness: {skewness:.2f}, Kurtosis: {kurtosis:.2f}")
    print(f"Answer rate: {answer_rate:.2f} answers per hour")
else:
    print("No answers to analyze.")
