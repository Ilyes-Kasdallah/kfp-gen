import kfp
from kfp.dsl import pipeline, component


@dsl.pipeline(name="fastq_processing")
def fastq_processing(
    fastq: str,
    leading: int = 0,
    trailing: int = 0,
    minlen: int = 0,
    sliding_window: int = 0,
):
    """
    Process a FASTQ file by trimming it according to specified parameters.

    Args:
    fastq (str): The path to the untrimmed FASTQ file.
    leading (int): The number of leading characters to trim.
    trailing (int): The number of trailing characters to trim.
    minlen (int): The minimum length of the trimmed sequence.
    sliding_window (int): The size of the sliding window for trimming.

    Returns:
    str: The path to the trimmed FASTQ file.
    """
    # Trim the FASTQ file using Trimmomatic
    trimmed_fastq = component.call(
        "trim",
        fastq=fastq,
        leading=leading,
        trailing=trailing,
        minlen=minlen,
        sliding_window=sliding_window,
    )

    return trimmed_fastq


# Example usage
fastq_file_path = "path/to/your/fastq/file.fastq"
trimmed_fastq_path = fastq_processing(fastq_file_path)
print(trimmed_fastq_path)
