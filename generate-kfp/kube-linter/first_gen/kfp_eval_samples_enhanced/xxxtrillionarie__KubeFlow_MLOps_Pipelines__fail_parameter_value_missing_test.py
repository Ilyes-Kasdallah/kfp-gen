from kfp import pipeline
from kfp.dsl import component


@component
def fail_parameter_value_missing_test():
    # This function should raise an error if the parameter is missing
    raise ValueError("Parameter 'missing_param' is missing")


@pipeline(name="data_processing_pipeline")
def data_processing_pipeline():
    # Define a single component that uses the fail_parameter_value_missing_test function
    process_data = component(
        name="process_data",
        description="Process data",
        inputs={
            "input_data": component.input("input_data"),
        },
        outputs={
            "processed_data": component.output("processed_data"),
        },
        steps=[
            component.step(
                name="process_data_step",
                description="Process data step",
                inputs={
                    "input_data": component.input("input_data"),
                },
                outputs={
                    "processed_data": component.output("processed_data"),
                },
                steps=[
                    component.step(
                        name="process_data_step2",
                        description="Process data step 2",
                        inputs={
                            "processed_data": component.input("processed_data"),
                        },
                        outputs={
                            "processed_data": component.output("processed_data"),
                        },
                    ),
                ],
            ),
        ],
    )


# Example usage of the pipeline
if __name__ == "__main__":
    process_data()
