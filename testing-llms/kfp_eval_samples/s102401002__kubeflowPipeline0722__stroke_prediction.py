```python
import kfp
from kfp import dsl

# Load data component
@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas==2.2.2"],
)
def load_data():
    # Read data from GitHub URLs
    # Perform data cleaning, handling missing values, mapping categorical features,
    # dropping unnecessary columns, removing specific rows, and shuffling the data
    # Output the preprocessed data as an Artifact
    pass

# Prepare data component
@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas==2.2.2", "scikit-learn==1.5.1"],
)
def prepare_data(data_input):
    # Take the preprocessed data from the load_data component
    # Split it into training, testing, and validation sets
    # Each output is a separate artifact
    pass

# Train model component
@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas==2.2.2", "scikit-learn==1.5.1"],
)
def train_model(X_train_output, Y_train_output, X_val_output, Y_val_output):
    # Take the training and validation data from the prepare_data component
    # Train a machine learning model for stroke prediction
    # Output the trained model as an Artifact
    pass

# Define the pipeline
@dsl.pipeline(name="Stroke Prediction Pipeline")
def stroke_prediction():
    # Load data
    load_data_task = load_data()
    
    # Prepare data
    prepare_data_task = prepare_data(load_data_task.outputs["data_output"])
    
    # Train model
    train_model_task = train_model(prepare_data_task.outputs["X_train_output"], 
                                   prepare_data_task.outputs["Y_train_output"], 
                                   prepare_data_task.outputs["X_val_output"], 
                                   prepare_data_task.outputs["Y_val_output"])

# Compile the pipeline
pipeline_spec = kfp.compiler.Compiler().compile(stroke_prediction)

# Submit the pipeline
client = kfp.Client()
experiment = client.create_experiment("My Experiment")
run = client.run(experiment.id, pipeline_name="Stroke Prediction Pipeline", pipeline_spec=pipeline_spec)
```

This code defines the required components and the pipeline structure, but the actual implementation of the `train_model` component is missing. You need to provide the specific details about the machine learning model and its hyperparameters to complete the pipeline.