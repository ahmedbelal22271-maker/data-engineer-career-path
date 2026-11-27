from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, StructField, StructType

# Initialize SparkSession connected to the Dockerized Spark Master
spark = (
    SparkSession.builder
    .master("spark://localhost:7077")
    .config("spark.executor.cores", "1")
    .config("spark.executor.memory", "512m")
    .getOrCreate()
)

# Create DataFrame with explicit schema
schema = StructType([
    StructField("id", IntegerType(), False),
    StructField("txt", StringType(), False),
])

data = [
    (1, "foo"),
    (2, "bar"),
]

df = spark.createDataFrame(data, schema)

# Output schema data types
print(df.dtypes)

# Display DataFrame contents
print("\nDataFrame:")
df.show()

spark.stop()
