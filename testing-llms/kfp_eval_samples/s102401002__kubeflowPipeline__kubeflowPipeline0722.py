```python
import kfp
from kfp import dsl

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split

# Load data component
@dsl.component(
    base_image='tensorflow/tensorflow:2.13.0',
    packages_to_install=['pandas', 'sklearn'],
    output_artifact_type=dsl.Artifact(type=dsl.ArtifactType.CSV)
)
def load_data(url1: str, url2: str) -> dsl.Artifact:
    # Download data from URLs
    df1 = pd.read_csv(url1)
    df2 = pd.read_csv(url2)

    # Concatenate datasets
    df = pd.concat([df1, df2], ignore_index=True)

    # Clean and preprocess data
    df.dropna(inplace=True)
    df['gender'] = df['gender'].map({'Male': 0, 'Female': 1})

    # Save cleaned dataset as CSV
    df.to_csv('cleaned_dataset.csv', index=False)

    return dsl.Artifact.from_file('cleaned_dataset.csv')

# Prepare data component
@dsl.component(
    base_image='tensorflow/tensorflow:2.13.0',
    packages_to_install=['pandas', 'sklearn'],
    input_artifact_types=[dsl.Artifact(type=dsl.ArtifactType.CSV)],
    output_artifact_types=[
        dsl.Artifact(type=dsl.ArtifactType.CSV),
        dsl.Artifact(type=dsl.ArtifactType.CSV),
        dsl.Artifact(type=dsl.ArtifactType.CSV),
        dsl.Artifact(type=dsl.ArtifactType.CSV)
    ]
)
def prepare_data(input_data: dsl.Artifact) -> dsl.Artifact:
    # Read cleaned dataset
    df = pd.read_csv(input_data.path)

    # Split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(df.drop('target', axis=1), df['target'], test_size=0.2, random_state=42)

    # Save split datasets as CSV
    x_train.to_csv('x_train.csv', index=False)
    x_test.to_csv('x_test.csv', index=False)
    y_train.to_csv('y_train.csv', index=False)
    y_test.to_csv('y_test.csv', index=False)

    return [
        dsl.Artifact.from_file('x_train.csv'),
        dsl.Artifact.from_file('x_test.csv'),
        dsl.Artifact.from_file('y_train.csv'),
        dsl.Artifact.from_file('y_test.csv')
    ]

# Main pipeline
@dsl.pipeline(name='diabetes_prediction_pipeline')
def diabetes_prediction_pipeline():
    # Load data
    load_data_task = load_data(url1='https://example.com/data1.csv', url2='https://example.com/data2.csv')

    # Prepare data
    prepare_data_task = prepare_data(input_data=load_data_task.output)

# Compile and run the pipeline
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(diabetes_prediction_pipeline, 'kubeflowPipeline0722.yaml')
    kfp.Client().create_run_from_pipeline_spec(
        pipeline_name='diabetes_prediction_pipeline',
        pipeline_root='/path/to/pipeline/root',
        pipeline_spec=open('kubeflowPipeline0722.yaml').read()
    )
```

This code snippet defines a Kubeflow Pipeline named `diabetes_prediction_pipeline` that performs diabetes prediction by loading data, cleaning and preprocessing it, splitting it into training and testing sets, and preparing these sets for further use. The pipeline is compiled and executed using the Kubeflow Pipelines SDK.