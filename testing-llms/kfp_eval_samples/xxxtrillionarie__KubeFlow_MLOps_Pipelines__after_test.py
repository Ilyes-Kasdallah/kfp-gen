```python
from kfp import dsl

# Define the Data Preparation component
@dsl.component(
    base_image="tensorflow/tensorflow:latest",
    outputs=["preprocessed_data"]
)
def data_preparation():
    # Placeholder for actual data preparation logic
    pass

# Define the Model Training component
@dsl.component(
    base_image="tensorflow/tensorflow:latest"
)
def model_training(prepared_data):
    # Placeholder for actual model training logic
    pass

# Define the main pipeline
@dsl.pipeline(name="my_pipeline")
def my_pipeline():
    # Call the Data Preparation component
    data_prep = data_preparation()
    
    # Call the Model Training component, passing the output of Data Preparation
    model_train = model_training(data_prep.outputs["preprocessed_data"])
```

This code defines a Kubeflow Pipeline named `my_pipeline` with two components: "Data Preparation" and "Model Training". The "Data Preparation" component is defined with an implicit name and outputs a single artifact. The "Model Training" component depends on the output of the "Data Preparation" component and does not produce any explicit output. The pipeline's control flow is sequential, with the "Model Training" component executing only after the "Data Preparation" component completes successfully.