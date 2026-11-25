import json
import sys
import time
from datetime import datetime, timedelta, timezone
from kafka import KafkaProducer

TOPIC = "campus-events"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    acks="all",
)

# Anchor today's UTC date at 08:10:00 so events span before and after the 08:15:00 threshold
base = datetime.now(timezone.utc).replace(hour=8, minute=10, second=0, microsecond=0)

# Default 7-event dataset (includes out-of-order and late > 08:15 events)
default_events = [
    ("S101", "check-in", "Computer Science", 120),      # 08:12:00 (on time)
    ("S204", "check-in", "Mathematics", 240),           # 08:14:00 (on time)
    ("S101", "open-course", "Computer Science", 300),   # 08:15:00 (ignored eventType)
    ("S305", "check-in", "Physics", 390),               # 08:16:30 (LATE > 08:15)
    ("S411", "check-in", "Computer Science", 510),      # 08:18:30 (LATE > 08:15)
    ("S204", "check-in", "Mathematics", 540),           # 08:19:00 (second check-in)
    ("S512", "check-in", "Physics", 180),               # 08:13:00 (on time, deliberately out of order)
]

# Optional stress-test mode: python producer.py --stress (sends 100 events for Section 11)
if "--stress" in sys.argv:
    import random
    departments = ["Computer Science", "Mathematics", "Physics"]
    event_types = ["check-in", "check-in", "check-in", "library-entry", "open-course"]
    events = []
    for i in range(100):
        student = f"S{random.randint(100, 140)}"
        etype = random.choice(event_types)
        dept = random.choice(departments)
        offset_sec = i * 3 - (35 if i % 10 == 0 else 0)  # periodic out-of-order events
        events.append((student, etype, dept, max(0, offset_sec)))
    delay = 0.05
else:
    events = default_events
    delay = 1.0

try:
    for event_id, (student, event_type, dept, seconds) in enumerate(events, 1):
        event_time = base + timedelta(seconds=seconds)
        event = {
            "eventId": event_id,
            "studentId": student,
            "eventType": event_type,
            "department": dept,
            "eventTime": event_time.isoformat(),
        }
        producer.send(TOPIC, value=event)
        print("Sent:", event)
        time.sleep(delay)

    producer.flush()
finally:
    producer.close()
