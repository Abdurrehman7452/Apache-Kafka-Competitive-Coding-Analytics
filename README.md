# Kafka Competitive Coding Analytics

This project simulates a real-time data processing system for competitive programming platforms using Apache Kafka. It ingests, processes, and analyzes structured submission events — such as problems, competitions, and solutions — to generate meaningful insights like top languages, hardest categories, leaderboards, and user ratings.

## 🔧 Tech Stack

- **Python 3**
- **Apache Kafka**
- **Kafka-Python (client)**
- **JSON & CLI**

---

## 📁 Project Structure
```
├── sampledata.txt # Input data simulating a live event stream
├── producer.py # Sends events from sampledata.txt to Kafka topics
├── consumer1.py # Analyzes most used language and hardest category
├── consumer2.py # Computes competition leaderboard scores
├── consumer3.py # Calculates user ELO ratings and best contributors
├── output1.json # Output from consumer1.py
├── output2.json # Output from consumer2.py
├── output3.json # Output from consumer3.py
```

---

## 📦 Kafka Topics

The data is divided and streamed into the following Kafka topics:
- `problem-events`
- `competition-events`
- `solution-events`

---

## 🚀 Getting Started

### 1. Start Kafka Server
Make sure Kafka and Zookeeper are up and running locally.

```bash
# Start Zookeeper (default)
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka broker
bin/kafka-server-start.sh config/server.properties
```

### 2. Create Topics

```bash
bin/kafka-topics.sh --create --topic problem-events --bootstrap-server localhost:9092
bin/kafka-topics.sh --create --topic competition-events --bootstrap-server localhost:9092
bin/kafka-topics.sh --create --topic solution-events --bootstrap-server localhost:9092
```

### 3. Run the Producer
```
cat sampledata.txt | ./producer.py problem-events competition-events solution-events
```

### 4. Run Consumers (in separate terminals)
```
./consumer1.py problem-events competition-events solution-events > output1.json
./consumer2.py problem-events competition-events solution-events > output2.json
./consumer3.py problem-events competition-events solution-events > output3.json
```

--- 

📊 Output Overview
consumer1.py — Language & Category Stats

    Identifies the most frequently used programming language.

    Determines the most difficult problem category (lowest pass ratio).

consumer2.py — Leaderboard Computation

    Calculates points per user using:

        Status score (Passed, TLE, Failed)

        Difficulty multiplier (Easy, Medium, Hard)

        Runtime bonus and time penalty

    Outputs a sorted leaderboard per competition.

consumer3.py — User Elo & Contributions

    Computes ELO-style ratings per user based on:

        Problem/competition submission scores

        Upvotes from accepted solutions

    Tracks the best contributor (most upvoted user).

---
📌 Notes

    All consumers exit gracefully on receiving the EOF signal.

    Runtime bonus boosts fast code, while time taken applies a penalty.

    Everything is designed to mimic low-latency real-time stream processing.

---

👨‍💻 Author

**Muhammad Abdurrehman**
_Bachelors in Data Science_
Loves building real-time data pipelines & making analytics transparent and simple.
