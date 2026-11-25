# TP06 — Real-Time Data Processing Using Apache Spark Structured Streaming and Apache Flink

**University of El Oued — Faculty of Exact Sciences — Department of Computer Science**  
**Program:** 2nd Year Master — AI & Data Science (2026/2027)  
**Module:** Big Data Analytics

## Software Versions
- **Python:** 3.11
- **Apache Kafka:** 3.x (via Docker container `tp05-kafka`)
- **kafka-python:** 2.0.2
- **Apache Spark / PySpark:** 3.5.3
- **Spark Kafka Connector:** `org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3` (Scala 2.12)
- **Apache Flink (SQL Analysis):** 1.18+

##Testing Guide

### 1. Start Kafka Broker & Create Topic
```bash
docker compose up -d

docker exec -it tp05-kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --create --if-not-exists --topic campus-events   --partitions 3 --replication-factor 1

docker exec -it tp05-kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092 --describe --topic campus-events
```

### 2. Virtual Environment
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Run Spark Streaming & Producer.py
Open **Terminal 1** (Spark Consumer):
```bash
spark-submit   --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3   spark_stream.py
```
i have created spark-temp in D partition
```bash
mkdir D:\spark-temp
spark-submit --conf "spark.local.dir=D:\spark-temp" --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 spark_stream.py
```
Open **Terminal 2** (Event Producer):
```bash
python producer.py
```
*(Optional Section 11 stress test with 100 events: `python producer.py --stress`)*

### 4. Cleanup
Stop Spark with `Ctrl+C`, then stop Kafka:
```bash
docker compose down
```
