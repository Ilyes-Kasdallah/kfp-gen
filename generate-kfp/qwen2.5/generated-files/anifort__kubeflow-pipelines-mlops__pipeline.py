
from kfp import pipeline
from kfp.components import component

@dsl.pipeline(name="A Simple CI Pipeline")
def simple_ci_pipeline():
    # Define a component that performs data preprocessing
    preprocess_component = component(
        name="Preprocess Data",
        description="This component performs basic data preprocessing tasks.",
        inputs={
            "data": {
                "type": "string",
                "description": "The input data to be processed."
            }
        },
        outputs={
            "cleaned_data": {
                "type": "string",
                "description": "The cleaned data after preprocessing."
            }
        },
        steps=[
            {
                "name": "Split Data",
                "task": "split_data",
                "inputs": {
                    "data": {
                        "value": "{{ data }}"
                    }
                },
                "outputs": {
                    "train_data": {
                        "value": "{{ data.split(',') }}"
                    },
                    "test_data": {
                        "value": "{{ data.split(',') }}"
                    }
                }
            },
            {
                "name": "Normalize Data",
                "task": "normalize_data",
                "inputs": {
                    "train_data": {
                        "value": "{{ train_data }}"
                    },
                    "test_data": {
                        "value": "{{ test_data }}"
                    }
                },
                "outputs": {
                    "normalized_train_data": {
                        "value": "{{ train_data.map(lambda x: (x - min(train_data)) / (max(train_data) - min(train_data))) }}"
                    },
                    "normalized_test_data": {
                        "value": "{{ test_data.map(lambda x: (x - min(test_data)) / (max(test_data) - min(test_data))) }}"
                    }
                }
            }
        ]
    )

    # Return the pipeline
    return preprocess_component
