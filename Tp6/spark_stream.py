from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    date_format,
    from_json,
    to_timestamp,
    window,
)
from pyspark.sql.types import IntegerType, StringType, StructField, StructType

spark = (
    SparkSession.builder
    .appName("CampusRealTimeAnalytics")
    .config("spark.sql.session.timeZone", "UTC")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("eventId", IntegerType(), True),
    StructField("studentId", StringType(), True),
    StructField("eventType", StringType(), True),
    StructField("department", StringType(), True),
    StructField("eventTime", StringType(), True),
])

raw = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "campus-events")
    .option("startingOffsets", "earliest")
    .option("failOnDataLoss", "false")
    .load()
)

json_events = raw.selectExpr("CAST(value AS STRING) AS json")

parsed = (
    json_events
    .select(from_json(col("json"), schema).alias("e"))
    .select("e.*")
    .withColumn("event_ts", to_timestamp(col("eventTime")))
    .filter(col("event_ts").isNotNull())
)

checkins = parsed.filter(col("eventType") == "check-in")

# Query 1 (Task 3): Department check-in counts in 1-minute event-time windows
counts = (
    checkins
    .withWatermark("event_ts", "30 seconds")
    .groupBy(
        window(col("event_ts"), "1 minute"),
        col("department"),
    )
    .count()
)

counts_query = (
    counts.writeStream
    .outputMode("update")
    .format("console")
    .option("truncate", "false")
    .option("checkpointLocation", "./checkpoint/campus-events-counts")
    .start()
)

# Query 2 (Task 5): Alert on late check-ins occurring after 08:15:00 UTC
late_checkins = (
    checkins
    .filter(date_format(col("event_ts"), "HH:mm:ss") > "08:15:00")
    .select("eventId", "studentId", "department", "eventTime")
)

late_query = (
    late_checkins.writeStream
    .outputMode("append")
    .format("console")
    .option("truncate", "false")
    .option("checkpointLocation", "./checkpoint/campus-events-late")
    .start()
)

spark.streams.awaitAnyTermination()
