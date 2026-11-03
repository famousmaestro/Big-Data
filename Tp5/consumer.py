import argparse
import csv
import json

from kafka import KafkaConsumer

parser = argparse.ArgumentParser()
parser.add_argument("--topic", default="campus-sensors")
parser.add_argument("--group", default="tp05-campus-monitor")
parser.add_argument("--building", default=None, help="filter, e.g. Building-A")
parser.add_argument("--csv", default=None, help="output file, e.g. events.csv")
args = parser.parse_args()

consumer = KafkaConsumer(
    args.topic,
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id=args.group,
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
)

FIELDS = ["event_id", "sensor_id", "temperature_c", "humidity_pct", "timestamp"]
csv_file = None
writer = None
if args.csv:
    csv_file = open(args.csv, "w", newline="", encoding="utf-8")
    writer = csv.DictWriter(csv_file, fieldnames=FIELDS, extrasaction="ignore")
    writer.writeheader()

total = 0.0
count = 0

print(f"Listening to topic: {args.topic} | group: {args.group} | filter: {args.building}")

try:
    for message in consumer:
        event = message.value
        temperature = event["temperature_c"]

        # running average over ALL received events
        count += 1
        total += temperature
        average = total / count

        # building filter (display only)
        if args.building and event.get("campus_building") != args.building:
            continue

        print(
            f'[p{message.partition}|off={message.offset}] '
            f'{event["timestamp"]} | {event["sensor_id"]} | '
            f'{event.get("campus_building")} | T={temperature}°C | '
            f'RH={event["humidity_pct"]}% | AVG={average:.2f}°C'
        )
        if temperature >= 35:
            print("ALERT: High temperature detected!")

        if writer:
            writer.writerow(event)
            csv_file.flush()
except KeyboardInterrupt:
    print(f"Consumer stopped. Events: {count}, final average: {total / max(count, 1):.2f}°C")
finally:
    consumer.close()
    if csv_file:
        csv_file.close()