# Databricks notebook source
# MAGIC %md
# MAGIC # Data Processing - Environment Aware
# MAGIC This notebook demonstrates environment-specific processing logic.
# MAGIC It receives environment parameters from the job definition.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Get Environment Parameters

# COMMAND ----------

import os
from datetime import datetime

# Get parameters from job (passed via databricks.yml variables)
catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
environment = dbutils.widgets.get("environment")

print(f"Running in {environment.upper()} environment")
print(f"Target: {catalog}.{schema}")
print(f"Timestamp: {datetime.now()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Environment-Specific Configuration

# COMMAND ----------

# Different behavior based on environment
if environment == "dev":
    # In dev, process smaller samples
    sample_fraction = 0.1
    checkpoint_interval = 100
    print("DEV Mode: Processing 10% sample, frequent checkpoints")
elif environment == "test":
    # In test, process more data with validation
    sample_fraction = 0.5
    checkpoint_interval = 50
    print("TEST Mode: Processing 50% sample, validation enabled")
elif environment == "prod":
    # In prod, process all data with optimizations
    sample_fraction = 1.0
    checkpoint_interval = 1000
    print("PROD Mode: Full data processing, optimized for performance")
else:
    raise ValueError(f"Unknown environment: {environment}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Schema if Not Exists

# COMMAND ----------

# Create schema for this environment
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")
spark.sql(f"USE {catalog}.{schema}")

print(f"Using schema: {catalog}.{schema}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Sample Data Processing

# COMMAND ----------

from pyspark.sql import functions as F

# Create sample data for demonstration
data = [
    (1, "Product A", 100.0, "2026-06-01"),
    (2, "Product B", 150.0, "2026-06-02"),
    (3, "Product C", 200.0, "2026-06-03"),
    (4, "Product D", 175.0, "2026-06-04"),
    (5, "Product E", 225.0, "2026-06-05"),
]

df = spark.createDataFrame(data, ["id", "product_name", "amount", "date"])

# Apply sampling based on environment
df_sampled = df.sample(fraction=sample_fraction, seed=42)

print(f"Original records: {df.count()}")
print(f"Sampled records: {df_sampled.count()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Write to Environment-Specific Table

# COMMAND ----------

# Write to environment-specific table
table_name = f"{catalog}.{schema}.processed_data"

df_sampled \
    .withColumn("processed_at", F.current_timestamp()) \
    .withColumn("environment", F.lit(environment)) \
    .write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(table_name)

print(f"Data written to: {table_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Validation and Logging

# COMMAND ----------

# Read back and validate
result_df = spark.table(table_name)
record_count = result_df.count()

print(f"\nValidation Results:")
print(f"  Records written: {record_count}")
print(f"  Environment: {environment}")
print(f"  Target table: {table_name}")

# Show sample
print(f"\nSample data:")
result_df.show(5, truncate=False)

# Environment-specific validation
if environment == "prod":
    # In production, ensure we have all records
    assert record_count == len(data), f"Production should process all records, got {record_count}"
    print("✓ Production validation passed")
elif environment == "test":
    # In test, verify environment column
    assert result_df.filter(F.col("environment") == "test").count() == record_count
    print("✓ Test validation passed")
else:
    print("✓ Dev validation passed")

print(f"\n{'='*50}")
print(f"SUCCESS: {environment.upper()} processing completed")
print(f"{'='*50}")
