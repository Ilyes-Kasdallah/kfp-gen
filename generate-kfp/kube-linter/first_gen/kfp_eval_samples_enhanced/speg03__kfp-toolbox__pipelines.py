import kfp
from kfp.dsl import pipeline, component


@dsl.pipeline(name="timestamp-pipeline")
def timestamp_pipeline():
    # Define the timestamp component
    @component
    def timestamp(timestamp_format):
        # Generate a timestamp string based on the provided format
        return f"{timestamp_format} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


# Example usage of the timestamp component
timestamp("YYYY-MM-DD HH:MM:SS")
