
from kfp import dsl

@dsl.pipeline(name='pipeline_from_func')
def pipeline_from_func():
    # Define the first component
    @dsl.component(name='process_data')
    def process_data(data):
        # Process the data here
        return data * 2

    # Define the second component
    @dsl.component(name='filter_data')
    def filter_data(data):
        # Filter the data here
        return data > 10

    # Define the third component
    @dsl.component(name='transform_data')
    def transform_data(data):
        # Transform the data here
        return data + 5

    # Define the fourth component
    @dsl.component(name='output_data')
    def output_data(data):
        # Output the processed data here
        return data

    # Define the pipeline
    @dsl.pipeline(name='pipeline_from_func')
    def pipeline_from_func():
        # Use the components in the pipeline
        processed_data = process_data(input_data)
        filtered_data = filter_data(processed_data)
        transformed_data = transform_data(filtered_data)
        output_data = output_data(transformed_data)

# Example usage
if __name__ == '__main__':
    pipeline_from_func()
