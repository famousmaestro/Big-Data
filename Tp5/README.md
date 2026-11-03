
# TP05 - Real-Time Data Streaming Using Apache Kafka

## 1. Project Overview

This project implements a real-time smart-campus monitoring
system using Apache Kafka, Python, and Docker Compose.

The system simulates temperature and humidity sensors,
publishes JSON events to a Kafka topic, and processes
incoming events to detect high-temperature conditions.

## 2. Technologies Used

- Apache Kafka 3.9.1
- Python 3.11
- kafka-python 2.0.2
- Docker
- Docker Compose
- JSON

## 3. Project Structure
```text
Tp5/
│
├── compose.yaml
├── requirements.txt
├── producer.py
├── consumer.py
├── README.md
│
└── screenshots/
```
## 4. Installation

Clone the repository:

```bash
git clone https://github.com/famousmaestro/Big-Data.git
cd Tp5
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## 5. Start Kafka in container named tp05-kafka

```bash
docker compose up -d
docker compose ps
docker compose logs --tail=50 kafka
```

## 6. Run the Producer

```bash
python producer.py
```

The producer generates 30 synthetic sensor events
and publishes them to the campus-sensors topic.

## 7. Run the Consumer

Open another terminal:

```bash
python consumer.py
```

The consumer reads sensor events and displays
temperature and humidity measurements.

It also detects high temperatures (>= 35°C).and print: Alert High Temperature

## 8. Kafka Topic Inspection

Create the topic:

```bash
docker exec -it tp05-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --if-not-exists --topic campus-sensors --partitions 3 --replication-factor 1
```

Describe the topic:

```bash
docker exec -it tp05-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic campus-sensors
```

List consumer groups:

```bash
docker exec -it tp05-kafka /opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
```

## 9. Report Questions

### Q1. What problem does Apache Kafka solve?

Apache Kafka reliably collects, stores, and distributes
continuous data streams between applications. It enables
real-time processing, scalability, and decoupling between
producers and consumers.

### Q2. Define Kafka components.

- Producer: Publishes messages.
- Consumer: Reads messages.
- Broker: Kafka server.
- Topic: Logical stream of messages.
- Partition: Subdivision of a topic.
- Offset: Message position inside a partition.
- Consumer Group: Group of consumers sharing the workload.

### Q3. Difference between Topic and Partition.

A topic organizes related messages, while a partition
is a subdivision of a topic that stores an ordered
sequence of messages.

### Q4. Why use auto_offset_reset='earliest'?

It allows a consumer to start from the earliest available
message when no valid committed offset exists.

### Q5. Purpose of consumer group ID.

It identifies a group of consumers and allows Kafka
to manage offsets and distribute partitions.
A new group ID has independent offsets.

### Q6. Why use JSON?

JSON is lightweight, readable, and easy to process.
One limitation is the lack of a strict built-in schema.

### Q7. How does Docker Compose simplify deployment?

It defines services and configurations in one YAML file
and allows easy deployment through simple commands.

### Q8. Limitations of a single-broker setup.

It has no broker redundancy, limited fault tolerance,
no high availability, and limited scalability.

### Q9. Evidence.

See the screenshots directory for:

1. Docker Compose status.
2. Kafka topic description.
3. Producer output.
4. Consumer output.

## 10. Problems Encountered
- First of all i had a latest version of python and when i tried to test on it it didn't work because doesn't support that version of kafka in the newest versions so i choose to use python version of 3.11 and the problem is fixed 

- In terminal when i try to run a command and i do not write the command right as an example i forget a char from topic name json will reject this beacuse when you create the topic you should keep writing the same name char by char
## 11. Conclusion

This practical work demonstrates how Apache Kafka
supports real-time event streaming and processing.

The project successfully simulates sensor events,
publishes JSON messages, consumes the stream,
and detects high-temperature conditions.
