
from pyspark.sql import SparkSession
import json

from dq_engine.core.rule_base import DQRule
from dq_engine.validator.validator_service import DQValidator
from dq_engine.reporter.summary_writer import write_json_summary
from dq_engine.reporter.html_report import generate_html_report
from dq_engine.rectifier.rectifier_service import DQRectifier

# Step 1: Start Spark
spark = SparkSession.builder.appName("DQ Engine").getOrCreate()

# Step 2: Load dataset
df = spark.read.option("header", True).csv("/path/to/forecast_data.csv")

# Step 3: Load rules from JSON
with open("dq_engine/config/rule_registry.json") as f:
    raw_rules = json.load(f)
rules = [DQRule(**r) for r in raw_rules]

# Step 4: Run Validator
validator = DQValidator(rules)
summary = validator.validate(df, table_name="forecast_data")

# Step 5: Write Reports
write_json_summary(summary, output_path="./dq_output")
generate_html_report(summary, output_path="./dq_output")

# Step 6: (Optional) Apply Rectifier
if not summary["execution_blocked"]:
    rectified_df = (
        DQRectifier(df)
        .fill_missing(column="forecast_val", strategy="ffill")
        .remove_outliers(column="forecast_val", threshold=3.0)
        .get_data()
    )
    rectified_df.write.mode("overwrite").parquet("/path/to/cleaned_output")

spark.stop()
