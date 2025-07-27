import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics

# Define the pipeline root
pipeline_root = "gs://my-bucket/pipeline-root"


# Define the component for training the LightGBM model
@dsl.component
def lightgbm_training(
    input_dataset: Dataset,
    input_params: dict,
    output_model: Model,
    output_dataset: Dataset,
    num_rounds: int = 10,
    max_depth: int = 10,
    min_samples_split: int = 2,
    min_samples_leaf: int = 1,
    learning_rate: float = 0.05,
    n_estimators: int = 100,
    random_state: int = 42,
    verbose: bool = False,
    cache: bool = True,
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Load the dataset
    dataset = Dataset.from_pandas(input_dataset)

    # Train the LightGBM model
    model = Model.from_kfp(
        image="gcr.io/<GCP PROJECT ID>/lightgbm-model:latest",
        input_data=dataset,
        params=input_params,
        output_model=output_model,
        output_dataset=output_dataset,
        num_rounds=num_rounds,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        learning_rate=learning_rate,
        n_estimators=n_estimators,
        random_state=random_state,
        verbose=verbose,
        cache=cache,
        retries=retries,
        resource_limits=resource_limits,
    )

    return model


# Define the pipeline
@dsl.pipeline(name="Kubeflow Fairing Pipeline")
def kubeflow_fairing_pipeline():
    # Define the input dataset
    input_dataset = Dataset.from_pandas("path/to/input_dataset.csv")

    # Define the input parameters
    input_params = {
        "feature_columns": ["feature1", "feature2"],
        "target_column": "target",
        "num_rounds": 10,
        "max_depth": 10,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "learning_rate": 0.05,
        "n_estimators": 100,
        "random_state": 42,
        "verbose": False,
        "cache": True,
        "retries": 2,
        "resource_limits": {"cpu": "1", "memory": "1Gi"},
    }

    # Define the output model
    output_model = Model.from_kfp(
        image="gcr.io/<GCP PROJECT ID>/lightgbm-model:latest",
        input_data=input_dataset,
        params=input_params,
        output_model=output_model,
        output_dataset=output_dataset,
        num_rounds=num_rounds,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        learning_rate=learning_rate,
        n_estimators=n_estimators,
        random_state=random_state,
        verbose=verbose,
        cache=cache,
        retries=retries,
        resource_limits=resource_limits,
    )

    # Define the output dataset
    output_dataset = Dataset.from_pandas("path/to/output_dataset.csv")

    # Define the pipeline
    pipeline = pipeline(
        steps=[
            lightgbm_training(
                input_dataset=input_dataset,
                input_params=input_params,
                output_model=output_model,
                output_dataset=output_dataset,
                num_rounds=num_rounds,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                min_samples_leaf=min_samples_leaf,
                learning_rate=learning_rate,
                n_estimators=n_estimators,
                random_state=random_state,
                verbose=verbose,
                cache=cache,
                retries=retries,
                resource_limits=resource_limits,
            )
        ],
        output=output_dataset,
    )

    # Compile the pipeline
    kfp.compiler.Compiler().compile(pipeline)


# Run the pipeline
kubeflow_fairing_pipeline()
