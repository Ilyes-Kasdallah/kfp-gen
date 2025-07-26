import kfp
from kfp.dsl import pipeline, component


@pipeline(name="My pipeline")
def norok_reusable_compo_pipeline(input_1_uri):
    """
    This pipeline performs a single operation using a reusable component.

    Args:
    input_1_uri (str): The URI of the text file to be processed.

    Returns:
    str: A message indicating the operation was successful.
    """

    # Define the echo component
    @component
    def echo(uri):
        """Echoes the content of the specified URI."""
        return f"Echoed content from {uri}"

    # Execute the echo component with the provided input
    result = echo(input_1_uri)

    # Return the result
    return result
