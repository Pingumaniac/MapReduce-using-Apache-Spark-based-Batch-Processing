rom pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count

spark = SparkSession.builder \
    .appName("WrongInferenceCount") \
    .getOrCreate()

df = spark.read \
    .format("mongo") \
    .option("spark.mongodb.input.uri", "mongodb://mongodb-service.team6.svc.cluster.local:27017/image_database.image_data") \
    .load()

wrong_inferences = df.withColumn(
    "is_wrong",
    when(col("InferredValue") != col("GroundTruth"), 1).otherwise(0)
)

result = wrong_inferences.groupBy("producer_id").agg(
    count(when(col("is_wrong") == 1, True)).alias("wrong_inference_count"),
    count("*").alias("total_inferences")
)

result = result.withColumn(
    "error_rate",
    (col("wrong_inference_count") / col("total_inferences") * 100)
)

print("Wrong Inference Counts by Producer:")
result.show()

result.write \
    .format("mongo") \
    .mode("overwrite") \
    .option("spark.mongodb.output.uri", "mongodb://10.82.1.62:27017/image_database.wrong_inference_stats") \
    .save()

spark.stop()
