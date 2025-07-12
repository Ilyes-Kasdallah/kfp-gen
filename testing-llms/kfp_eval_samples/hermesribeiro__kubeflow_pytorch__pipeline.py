```python
from kfp import dsl
from kfp.aws import use_aws_secret

# Define the Model Train component
@dsl.component(
    base_image="hermesribeiro/cifar:latest",
    requirements=[
        {
            "name": "pytorch",
            "version": "1.9.0"
        },
        {
            "name": "tensorboard",
            "version": "2.8.0"
        }
    ],
    metadata={
        "pip_requirements": [
            "torch==1.9.0",
            "tensorboard==2.8.0"
        ]
    },
    annotations={
        "mlflow.runName": "CIFAR Pytorch Training",
        "mlflow.tags": {
            "framework": "PyTorch",
            "dataset": "CIFAR-10"
        }
    }
)
def train(num_epochs: int, batch_size: int, learning_rate: float, momentum: float, bucket: str, path: str):
    # Implementation of the train.py script
    pass

# Define the Model Eval component
@dsl.component(
    base_image="hermesribeiro/cifar:latest",
    requirements=[
        {
            "name": "pytorch",
            "version": "1.9.0"
        }
    ],
    metadata={
        "pip_requirements": [
            "torch==1.9.0"
        ]
    },
    annotations={
        "mlflow.runName": "CIFAR Pytorch Evaluation",
        "mlflow.tags": {
            "framework": "PyTorch",
            "dataset": "CIFAR-10"
        }
    }
)
def eval(bucket: str, path: str):
    # Implementation of the eval.py script
    pass

# Define the main pipeline
@dsl.pipeline(name="CIFAR Pytorch")
def cifar_pytorch_pipeline():
    # Train the model
    train_op = train(
        num_epochs=10,
        batch_size=64,
        learning_rate=0.01,
        momentum=0.9,
        bucket="your-bucket-name",
        path="your-path-in-bucket"
    )

    # Evaluate the model
    eval_op = eval(
        bucket="your-bucket-name",
        path="your-path-in-bucket"
    )

    # Set up dependencies
    train_op.after(eval_op)

# Execute the pipeline
if __name__ == "__main__":
    kfp.compiler.Compiler().compile(cifar_pytorch_pipeline, "cifar_pytorch_pipeline.yaml")
```

In this solution, we define two components: `train` and `eval`, each using the same Docker image and requiring specific PyTorch versions. We then define a main pipeline that orchestrates these components sequentially. The `after` method is used to specify that the `eval` component should run only after the `train` component has completed. Finally, we compile the pipeline into a YAML file using the `kfp.compiler.Compiler()` class.