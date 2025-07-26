import kfp
from kfp.dsl import pipeline, component

# Define the pipeline function name
pipeline_name = "viai-retrain"


# Define the check_files function using a Docker container image
@component(image="tseo/check_bucket:0.3")
def check_files(bucket_name):
    # Check if the bucket exists
    if not kfp.io.gcs.GCSBucket(bucket_name).exists():
        raise ValueError(f"Bucket {bucket_name} does not exist.")

    # Count the number of files in the bucket
    num_files = len(kfp.io.gcs.GCSBucket(bucket_name).list())

    # Output the results
    return {"file_nums": num_files}


# Define the viai_retrain function using the check_files function
@pipeline(name=pipeline_name)
def viai_retrain(bucket_name):
    # Call the check_files function to get the number of files
    result = check_files(bucket_name)

    # Print the result
    print(result)


# Run the pipeline
viai_retrain("your-bucket-name")
