import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from kfp.components import PythonComponent


# Define the pipeline
@pipeline(name="lightweight_python_functions_v2_with_outputs")
def lightweight_python_functions_v2_with_outputs():
    # Define the first component
    @component(name="component_1")
    def generate_strings():
        # Generate two strings
        first_string = "first"
        second_string = "second"
        # Write the strings to separate files
        with open("output1.txt", "w") as file:
            file.write(first_string)
        with open("output2.txt", "w") as file:
            file.write(second_string)
        return first_string, second_string

    # Define the second component
    @component(name="component_2")
    def write_to_file(file_path, content):
        # Write content to a file
        with open(file_path, "w") as file:
            file.write(content)
        return f"Content written to {file_path}"

    # Define the third component
    @component(name="component_3")
    def process_data(data):
        # Process the data (example: convert to uppercase)
        processed_data = data.upper()
        return processed_data

    # Call the components
    first_output, second_output = generate_strings()
    processed_output = process_data(first_output)

    # Write the processed output to a file
    write_to_file("processed_output.txt", processed_output)


# Run the pipeline
if __name__ == "__main__":
    lightweight_python_functions_v2_with_outputs()
