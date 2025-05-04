#!/usr/bin/env python3
import sys
import json
import math
from kafka import KafkaConsumer
from collections import defaultdict

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: ./consumer3.py topicName1 topicName2 topicName3")
        sys.exit(1)

    # define consumers for topics
    topic_problem = sys.argv[1]
    topic_competition = sys.argv[2]
    topic_solution = sys.argv[3]
    consumer = KafkaConsumer(topic_problem, topic_competition, topic_solution,
                             bootstrap_servers='localhost:9092',
                             value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                             consumer_timeout_ms=5000)

    # track user elo ratings and upvotes
    user_elo = defaultdict(lambda: 1200)
    user_upvotes = defaultdict(int)

    K = 32  

    # process incoming data
    for message in consumer:
        parts = message.value

        if parts == ["EOF"]:
            print("EOF received, exiting.")
            break

        if parts[0] == "problem":
            _, user_id, problem_id, category, difficulty, submission_id, status, language, runtime = parts

            # calculate Status_Score
            if status == "Passed":
                status_score = 1
            elif status == "TLE":
                status_score = 0.2
            else:
                status_score = -0.3

            # calculate Difficulty_Score
            if difficulty == "Hard":
                difficulty_score = 1
            elif difficulty == "Medium":
                difficulty_score = 0.7
            else:
                difficulty_score = 0.3

            runtime_bonus = 10000 / float(runtime)   # calculate Runtime_Bonus

            submission_points = K * (status_score * difficulty_score) + runtime_bonus  # calculate Submission_Points

            user_elo[user_id] += submission_points  # update user's elo rating

        elif parts[0] == "competition":
            _, comp_id, user_id, com_problem_id, category, difficulty, comp_submission_id, status, language, runtime, time_taken = parts

            # calculate Status_Score
            if status == "Passed":
                status_score = 1
            elif status == "TLE":
                status_score = 0.2
            else:
                status_score = -0.3

            # calculate Difficulty_Score
            if difficulty == "Hard":
                difficulty_score = 1
            elif difficulty == "Medium":
                difficulty_score = 0.7
            else:
                difficulty_score = 0.3
            
            runtime_bonus = 10000 / float(runtime)  # calculate Runtime_Bonus
            
            submission_points = K * (status_score * difficulty_score) + runtime_bonus  # calculate Submission_Points
            
            user_elo[user_id] += submission_points  # update user's elo rating

        elif parts[0] == "solution":
            _, user_id, problem_id, submission_id, upvotes = parts
            
            user_upvotes[user_id] += int(upvotes)  # track user upvotes

    # best contributor (most upvotes)
    max_upvotes = max(user_upvotes.values(), default=0)
    best_contributor = sorted([user for user, upvote_count in user_upvotes.items() if upvote_count == max_upvotes])

    # floor elo ratings and sort 
    sorted_user_elo = {user: math.floor(elo) for user, elo in sorted(user_elo.items())}


    result = {
        "best_contributor": best_contributor,
        "user_elo_rating": sorted_user_elo
    }

    print(json.dumps(result, indent=4))

