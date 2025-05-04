#!/usr/bin/env python3
import sys
import json
from kafka import KafkaProducer

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: ./producer.py topicName1 topicName2 topicName3")
        sys.exit(1)

    topic_problem = sys.argv[1]
    topic_competition = sys.argv[2]
    topic_solution = sys.argv[3]

    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    for line in sys.stdin:
        if line.strip() == "EOF":
            break
        parts = line.strip().split()
        event_type = parts[0]

        # Send message to the corresponding Kafka topic
        if event_type == "problem":
            producer.send(topic_problem, value=parts)
        elif event_type == "competition":
            producer.send(topic_competition, value=parts)
        elif event_type == "solution":
            producer.send(topic_solution, value=parts)

    producer.flush()
    producer.close()

