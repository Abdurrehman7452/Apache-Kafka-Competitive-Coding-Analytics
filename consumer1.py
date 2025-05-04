#!/usr/bin/env python3
import sys
import json
from kafka import KafkaConsumer
from collections import defaultdict

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: ./consumer1.py topicName1 topicName2 topicName3")
        sys.exit(1)

    topic_problem = sys.argv[1]
    consumer = KafkaConsumer(topic_problem, bootstrap_servers='localhost:9092',
                             value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                             consumer_timeout_ms=5000)

    lang_count = defaultdict(int)  # track language frequency
    cat_stats = defaultdict(lambda: {'passed': 0, 'total': 0})  # track submission stats

    # process message data
    for message in consumer:
        parts = message.value

        if parts == ["EOF"]:
            print("EOF received, exiting.")
            break

        if parts[0] == "problem":
            _, user_id, problem_id, category, difficulty, submission_id, status, language, runtime = parts

            lang_count[language] += 1
            cat_stats[category]['total'] += 1
            if status == "Passed":
                cat_stats[category]['passed'] += 1
            
            
    # analyze language usage
    if lang_count:
        lang_max_count = max(lang_count.values())
        freq_most_lang = sorted([lang for lang, count in lang_count.items() if count == lang_max_count])
    else:
        freq_most_lang = []


    # calculate category difficulty
    minpass_ratio = float('inf')
    diff_most_catg = []

    for category, stats in cat_stats.items():
        if stats['total'] > 0:
            pass_ratio = stats['passed'] / stats['total']
            if pass_ratio < minpass_ratio:
                minpass_ratio = pass_ratio
                diff_most_catg = [category]
            elif pass_ratio == minpass_ratio:
                diff_most_catg.append(category)

    diff_most_catg = sorted(diff_most_catg)


    result = {
        "most_used_language": freq_most_lang,
        "most_difficult_category": diff_most_catg
    }

    print(json.dumps(result, indent=4))

