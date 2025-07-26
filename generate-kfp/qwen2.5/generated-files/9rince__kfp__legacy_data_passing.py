
from kfp import pipeline
from kfp.components import legacy_data_passing

@pipeline(name="data_passing_pipeline")
def data_passing_pipeline():
    # Scenario 1: Constant value passing
    @legacy_data_passing(value=10)
    def pass_constant_value():
        return "Constant Value"

    # Scenario 2: Pipeline parameter passing
    @legacy_data_passing(parameter="example_param")
    def pass_pipeline_parameter(param):
        return f"Parameter Value: {param}"

    # Scenario 3: Component output consumption
    @legacy_data_passing(output="output_file")
    def consume_component_output(component_output):
        return component_output

    # Scenario 4: File consumption
    @legacy_data_passing(file_path="file.txt")
    def consume_file(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        return content

    # Scenario 5: Data type conversion
    @legacy_data_passing(data_type="int")
    def convert_data_type(data):
        return int(data)

    # Scenario 6: Data type conversion from string
    @legacy_data_passing(data_type="str")
    def convert_string_to_int(data):
        return int(data)

# Example usage
if __name__ == "__main__":
    data_passing_pipeline().execute()
