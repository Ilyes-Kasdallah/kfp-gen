import kfp
from kfp import dsl
from kfp.components import load_component_from_text

# Define the Spark component
spark_component = load_component_from_text("""
name: Spark Weather Job
description: Runs the Spark job to process weather data.
implementation:
    container:
        image: spark-weather-job:latest
        command:
        - spark-submit
        - /app/spark-job.py
""")

@dsl.pipeline(
    name="Spark Weather Pipeline",
    description="A pipeline that runs a Spark job to process weather data."
)
def spark_weather_pipeline():
    # Add the Spark component to the pipeline
    spark_task = spark_component()

# Compile the pipeline for v1 compatibility
if __name__ == "__main__":
    kfp.compiler.Compiler().compile(
        pipeline_func=spark_weather_pipeline,
        package_path="kubeflow-pipeline/spark_weather_pipeline.yaml"
    )
