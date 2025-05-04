#!/usr/bin/env python3
import sys
import json
from kafka import KafkaConsumer
from collections import defaultdict
import math

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: ./consumer2.py topicName1 topicName2 topicName3")
        sys.exit(1)


    topic_competition = sys.argv[2]
    consumer = KafkaConsumer(topic_competition, bootstrap_servers='localhost:9092',
                             value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                             consumer_timeout_ms=5000)

    
    leaderboard = defaultdict(lambda: defaultdict(int))  # track leaderboard points

    # process incoming data
    for message in consumer:
        parts = message.value

        if parts == ["EOF"]:
            print("EOF received, exiting.")
            break

        if parts[0] == "competition":
            _, comp_id, user_id, com_problem_id, category, difficulty, comp_submission_id, status, language, runtime, time_taken = parts

            # calculate Status_Score
            if status == "Passed":
                status_score = 100
            elif status == "TLE":
                status_score = 20
            else:
                status_score = 0

            # calculate Difficulty_Score
            if difficulty == "Hard":
                difficulty_score = 3
            elif difficulty == "Medium":
                difficulty_score = 2
            else:
                difficulty_score = 1

            # calculate Bonus
            runtime_bonus = 10000 / float(runtime)
            time_taken_penalty = 0.25 * float(time_taken)
            bonus = max(1, (1 + runtime_bonus - time_taken_penalty))
        
            submission_points = status_score * difficulty_score * bonus  # calculate submission points
            
            leaderboard[comp_id][user_id] += math.floor(submission_points)  # round down points and update leaderboard


    sorted_leaderboard = {comp: dict(sorted(users.items())) for comp, users in sorted(leaderboard.items())}


    print(json.dumps(sorted_leaderboard, indent=4))

