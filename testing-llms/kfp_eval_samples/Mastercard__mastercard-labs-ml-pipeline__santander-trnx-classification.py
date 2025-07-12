```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load components from files
tf_transform = load_component_from_file('path/to/tf-transform.yaml')
tf_train = load_component_from_file('path/to/tf-train.yaml')
tf_predict = load_component_from_file('path/to/tf-predict.yaml')
confusion_matrix = load_component_from_file('path/to/confusion-matrix.yaml')
roc = load_component_from_file('path/to/roc.yaml')
deploy = load_component_from_file('path/to/deploy.yaml')

# Define the pipeline
@sdk.pipeline(name='Santander Customer Transaction Prediction')
def santander_trnx_classification(
    train_path: str,
    evaluation_path: str,
    project: str,
    mode: str,
    preprocess_module: str,
    platform: str
):
    # Dataflow TF Transform
    transform_op = tf_transform(
        train_path=train_path,
        evaluation_path=evaluation_path,
        project=project,
        mode=mode,
        preprocess_module=preprocess_module
    )

    # TF Train
    train_op = tf_train(
        transformed_data_dir=transform_op.outputs['transformed_data_dir'],
        schema='path/to/not.txt',
        learning_rate=0.01,
        hidden_layer_size=128,
        steps=1000,
        target_column='tips',
        preprocess_module=preprocess_module,
        training_output_dir=transform_op.outputs['training_output_dir']
    )

    # Dataflow TF Predict
    predict_op = tf_predict(
        evaluation=evaluation_path,
        schema='path/to/not.txt',
        target_column='tips',
        training_output_dir=train_op.outputs['training_output_dir'],
        mode=mode,
        project=project
    )

    # Confusion Matrix
    confusion_matrix_op = confusion_matrix(
        predictions=predict_op.outputs['predictions']
    )

    # ROC
    roc_op = roc(
        predictions=predict_op.outputs['predictions']
    )

    # Kubeflow Deploy
    deploy_op = deploy(
        trained_model_dir=train_op.outputs['training_output_dir']
    )

    # Conditional logic based on platform
    if platform != 'GCP':
        # Add volume operation and git checkout step
        pass

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(santander_trnx_classification, 'santander-trnx-classification.yaml')
```

This code snippet defines a Kubeflow Pipeline named `Santander Customer Transaction Prediction` that performs customer transaction classification using Apache Beam and TensorFlow. The pipeline includes components for data preprocessing, model training, prediction, confusion matrix calculation, ROC curve generation, and deployment. The pipeline uses Kubeflow Pipelines (kfp), TensorFlow, Apache Beam, and potentially other libraries within the loaded component YAML files. The pipeline uses GCS for data storage.