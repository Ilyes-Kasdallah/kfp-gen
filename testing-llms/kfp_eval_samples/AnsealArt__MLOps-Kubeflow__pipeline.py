```python
import kfp
from kfp import dsl

# Define the pipeline
@dsl.pipeline(name="California Housing prediction Pipeline")
def california_housing_prediction_pipeline(test_size=0.2, output_path="/tmp", deployment_threshhold_mse=None):
    # Download and preprocess data
    download_and_preprocess = dsl.ContainerOp(
        name="download-and-preprocess",
        image="dzieciolfilipit/kf_ch_preprocess_data:1.1",
        arguments=[
            "--output-path", output_path,
            "--run-date", dsl.RUN_DATE,
            "--test-size", str(test_size)
        ]
    )

    # Train SGD Regressor
    train_sgd_regressor = dsl.ContainerOp(
        name="train-sgd-regressor",
        image="dzieciolfilipit/kf_ch_train_model:1.1",
        arguments=[
            "--x-train", f"{output_path}/x_train.npy",
            "--y-train", f"{output_path}/y_train.npy",
            "--output-path", output_path,
            "--run-date", dsl.RUN_DATE
        ],
        dependencies=[download_and_preprocess]
    )

    # Test model and get MSE metric
    test_model_and_get_mse = dsl.ContainerOp(
        name="test-model-and-get-mse",
        image="dzieciolfilipit/kf_ch_test_model:1.1",
        arguments=[
            "--x-test", f"{output_path}/x_test.npy",
            "--y-test", f"{output_path}/y_test.npy",
            "--model-path", f"{output_path}/model.pkl",
            "--output-path", output_path,
            "--run-date", dsl.RUN_DATE
        ],
        dependencies=[train_sgd_regressor]
    )

    # Deploy model for inference
    deploy_model_for_inference = dsl.ContainerOp(
        name="deploy-model-for-inference",
        image="dzieciolfilipit/kf_ch_deploy_model:1.1",
        arguments=[
            "--model-path", f"{output_path}/model.pkl",
            "--mse-path", f"{output_path}/mse.txt"
        ],
        dependencies=[test_model_and_get_mse]
    )
```

This code defines a Kubeflow Pipeline named `California Housing prediction Pipeline` with the specified components and their dependencies. The pipeline uses the Docker images `dzieciolfilipit/kf_ch_preprocess_data:1.1`, `dzieciolfilipit/kf_ch_train_model:1.1`, `dzieciolfilipit/kf_ch_test_model:1.1`, and `dzieciolfilipit/kf_ch_deploy_model:1.1`. The pipeline takes `test_size`, `output_path`, and `deployment_threshhold_mse` as parameters.