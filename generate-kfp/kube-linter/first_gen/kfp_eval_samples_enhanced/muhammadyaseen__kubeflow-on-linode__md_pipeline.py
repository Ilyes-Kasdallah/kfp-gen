from kfp import pipeline
from kfp.dsl import component


@component
def write_simple_markdown_table():
    """
    Creates a Markdown file containing a simple table with animal names.

    Returns:
        str: A string representation of a Markdown table.
    """
    # Define the table data
    animal_names = ["Dog", "Cat", "Elephant", "Fox"]
    table_data = [["Name", "Age"], ["Dog", 3], ["Cat", 5], ["Elephant", 7], ["Fox", 9]]

    # Create the Markdown table string
    markdown_table = f"""
| Name | Age |
|------|------|
| Dog   | 3   |
| Cat   | 5   |
| Elephant| 7   |
| Fox   | 9   |
    """

    # Return the Markdown table string
    return markdown_table


@pipeline(name="md-pipeline")
def md_pipeline():
    """
    Runs the `write_simple_markdown_table` component.
    """
    # Call the component and get the output
    result = write_simple_markdown_table()

    # Print the result
    print(result)


# Run the pipeline
if __name__ == "__main__":
    md_pipeline()
