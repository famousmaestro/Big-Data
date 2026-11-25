-- Task 6: Apache Flink SQL Event-Time Window Analysis
-- Compatible with Apache Flink 1.18+ and flink-sql-connector-kafka

CREATE TABLE campus_events (
    eventId INT,
    studentId STRING,
    eventType STRING,
    department STRING,
    eventTime TIMESTAMP(3),
    WATERMARK FOR eventTime AS eventTime - INTERVAL '30' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'campus-events',
    'properties.bootstrap.servers' = 'localhost:9092',
    'properties.group.id' = 'tp06-flink',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'json',
    'json.timestamp-format.standard' = 'ISO-8601'
);

SELECT
    window_start,
    window_end,
    department,
    COUNT(*) AS checkins
FROM TABLE(
    TUMBLE(
        TABLE campus_events,
        DESCRIPTOR(eventTime),
        INTERVAL '1' MINUTE
    )
)
WHERE eventType = 'check-in'
GROUP BY window_start, window_end, department;
