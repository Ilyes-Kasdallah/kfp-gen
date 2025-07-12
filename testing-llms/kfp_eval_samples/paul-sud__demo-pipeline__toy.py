```python
from kfp import dsl
from kfp.components import func_to_container_op

# Define the trim component
@dsl.component(
    base_image="quay.io/encode-dcc/demo-pipeline:template",
    packages_to_install=["java", "trimmomatic"]
)
def trim(fastq: str, leading: int = 3, trailing: int = 3, minlen: int = 50, sliding_window: int = 4):
    # Trim the FASTQ file using Trimmomatic
    command = [
        "/software/Trimmomatic-0.38/trimmomatic-0.38.jar",
        "-threads", "4",
        "-phred33",
        fastq,
        f"{fastq}_unpaired.fastq",
        f"{fastq}_paired.fastq",
        f"{fastq}_unpaired.fastq.gz",
        f"{fastq}_paired.fastq.gz"
    ]
    return func_to_container_op(command)

# Define the plot component
@dsl.component(
    base_image="quay.io/encode-dcc/demo-pipeline:template",
    packages_to_install=["matplotlib"]
)
def plot(fastq: str, trimmed_fastq: str, bar_color: str = "blue", flier_color: str = "red", plot_color: str = "green"):
    # Plot the quality scores using a Python script
    command = [
        "/software/demo-pipeline/src/plot_fastq_scores.py",
        fastq,
        trimmed_fastq,
        bar_color,
        flier_color,
        plot_color
    ]
    return func_to_container_op(command)

# Define the toy pipeline
@dsl.pipeline(name="fastq_processing")
def toy():
    # Call the trim component
    trimmed_fastq = trim("input.fastq")

    # Call the plot component
    plot(trimmed_fastq, "input.fastq", bar_color="blue", flier_color="red", plot_color="green")
```

This code snippet defines a Kubeflow Pipeline named `fastq_processing` that includes two components: `trim` and `plot`. The `trim` component uses Trimmomatic to process FASTQ files, while the `plot` component generates a quality score plot based on the processed data. The pipeline's control flow is sequential, with the `plot` component depending on the output of the `trim` component. Both components are executed within Docker containers with specific configurations.