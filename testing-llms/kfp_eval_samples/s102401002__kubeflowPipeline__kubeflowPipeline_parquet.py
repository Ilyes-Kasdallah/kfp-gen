```python
import kfp
from kfp import dsl
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import requests
import pyarrow.parquet as pq

# Load data component
@dsl.component(
    base_image="python:3.9",
    packages_to_install=[
        "pandas", "numpy", "requests", "pyarrow"
    ]
)
def load_data(input_url: str, output_file: dsl.OutputPath):
    # Load data from URL
    response = requests.get(input_url)
    data = response.json()
    
    # Handle missing values
    data = data.dropna(subset=['age', 'bmi', 'HbA1c_level', 'blood_glucose_level'])
    
    # Convert categorical features to numerical
    data['gender'] = data['gender'].map({'Male': 0, 'Female': 1})
    
    # Convert age, bmi, HbA1c_level, and blood_glucose_level to numeric
    data[['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']] = data[['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']].astype(float)
    
    # Fill in missing values with mean
    data.fillna(data.mean(), inplace=True)
    
    # Save data to Parquet file
    pq.write_table(pd.DataFrame(data), output_file.path)

# Prepare data component
@dsl.component(
    base_image="python:3.9",
    packages_to_install=[
        "pandas", "scikit-learn", "pyarrow"
    ]
)
def prepare_data(input_file: dsl.InputPath, output_x_train: dsl.OutputPath, output_x_test: dsl.OutputPath, output_y_train: dsl.OutputPath, output_y_test: dsl.OutputPath):
    # Load data from Parquet file
    df = pd.read_parquet(input_file.path)
    
    # Split data into training and testing sets
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Save each set to separate Parquet file
    pq.write_table(x_train, output_x_train.path)
    pq.write_table(x_test, output_x_test.path)
    pq.write_table(y_train, output_y_train.path)
    pq.write_table(y_test, output_y_test.path)

# Train model component
@dsl.component(
    base_image="python:3.9",
    packages_to_install=[
        "pandas", "scikit-learn", "joblib", "pyarrow"
    ]
)
def train_model(input_x_train: dsl.InputPath, input_y_train: dsl.InputPath, output_model: dsl.OutputPath):
    # Load data from Parquet files
    x_train_df = pd.read_parquet(input_x_train.path)
    y_train_df = pd.read_parquet(input_y_train.path)
    
    # Train logistic regression model
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(max_iter=1000)
    model.fit(x_train_df, y_train_df)
    
    # Save model to joblib file
    joblib.dump(model, output_model.path)

# Main pipeline
@dsl.pipeline(name="diabetes_prediction_pipeline")
def diabetes_prediction_pipeline():
    # Load data
    load_data_task = load_data(input_url="https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/pima-indians-diabetes.csv", output_file=dsl.OutputPath("data.parquet"))
    
    # Prepare data
    prepare_data_task = prepare_data(input_file=load_data_task.outputs["output_file"], output_x_train=dsl.OutputPath("x_train.parquet"), output_x_test=dsl.OutputPath("x_test.parquet"), output_y_train=dsl.OutputPath("y_train.parquet"), output_y_test=dsl.OutputPath("y_test.parquet"))
    
    # Train model
    train_model_task = train_model(input_x_train=prepare_data_task.outputs["output_x_train"], input_y_train=prepare_data_task.outputs["output_y_train"], output_model=dsl.OutputPath("model.joblib"))

# Compile and run the pipeline
if __name__ == "__main__":
    kfp.compiler.Compiler().compile(diabetes_prediction_pipeline, "kubeflowPipeline_parquet.py")
    kfp.Client().create_run_from_pipeline_package("kubeflowPipeline_parquet.py", arguments={})
```

This code defines a Kubeflow Pipeline named `diabetes_prediction_pipeline` that performs diabetes prediction using a Logistic Regression model. The pipeline consists of three components: `load_data`, `prepare_data`, and `train_model`. Each component is defined using the `@dsl.component` decorator with appropriate inputs and outputs. The pipeline's control flow is sequential, and no parallel processing is used. The pipeline utilizes Python 3.9 as the base image for all components.