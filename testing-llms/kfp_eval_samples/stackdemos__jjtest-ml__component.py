```python
import kfp
from kfp import dsl
from urllib.parse import urlparse

# Define the global variable for the training image
TRAINING_IMAGE = "your/training/image"

# Data Download Component
@dsl.component(
    base_image="appropriate/curl",
    outputs=["output_file"],
    requirements=[
        {
            "name": "curl",
            "version": "7.64.0"
        }
    ]
)
def download_artifact(url: str, local_path: str, md5_checksum: str):
    # Check if the file already exists locally
    if os.path.exists(local_path):
        print(f"File {local_path} already exists.")
        return
    
    # Download the file using curl
    subprocess.run(["curl", "-o", local_path, url], check=True)
    
    # Calculate the MD5 checksum of the downloaded file
    actual_md5 = hashlib.md5(open(local_path, 'rb').read()).hexdigest()
    
    # Compare the calculated MD5 checksum with the expected one
    if actual_md5 == md5_checksum:
        print("MD5 checksum matches, skipping download.")
    else:
        print(f"MD5 checksum mismatch. Expected {md5_checksum}, got {actual_md5}.")
        raise Exception("Download failed due to MD5 checksum mismatch.")

# Model Training Component
@dsl.component(
    base_image=TRAINING_IMAGE,
    outputs=file_outputs,
    requirements=[
        {
            "name": "python",
            "version": "3.8"
        },
        {
            "name": "scikit-learn",
            "version": "0.24.2"
        }
    ],
    ins={"input_file": dsl.InputArtifact(type=dsl.ArtifactType.FILE)}
)
def training_op(input_file: dsl.InputArtifact):
    # Read the input file
    with open(input_file.path, 'r') as f:
        data = f.read()
    
    # Perform some processing on the data
    processed_data = process_data(data)
    
    # Save the processed data to an output artifact
    output_file.save(processed_data)

# Main Pipeline
@dsl.pipeline(name="my_pipeline")
def my_pipeline():
    # Download the data
    http_download_op = download_artifact(
        url="https://example.com/dataset.zip",
        local_path="/tmp/dataset.zip",
        md5_checksum="expected_md5_checksum"
    )
    
    # Train the model
    training_op(input_file=http_download_op.output_file)
```

In this solution, we define two components: `download_artifact` and `training_op`. The `download_artifact` component downloads a file from a given URL and checks its MD5 checksum against an expected value. If the checksum matches, it skips the download. The `training_op` component reads the downloaded file, processes it, and saves the result as an output artifact. The main pipeline orchestrates these components in sequence.