
from kfp import pipeline
from kfp.components import component

@component
def fail_parameter_value_missing_test():
    # This function should raise an error if the parameter 'value' is missing
    raise ValueError("Parameter 'value' is missing")

@pipeline(name="simple-data-processing-pipeline")
def simple_data_processing_pipeline():
    # Define the task
    task = fail_parameter_value_missing_test()
    
    # Define the pipeline steps
    step1 = task()
    step2 = task()
    
    # Define the pipeline execution
    return step1 + step2

# Example usage
if __name__ == "__main__":
    result = simple_data_processing_pipeline()
    print(result)
