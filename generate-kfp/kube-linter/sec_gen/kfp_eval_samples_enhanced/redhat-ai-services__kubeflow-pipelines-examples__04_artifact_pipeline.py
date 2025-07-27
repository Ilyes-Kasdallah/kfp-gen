import kfp
from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics

# Define the base image for the artifact creation
base_image = "image-registry.openshift-image-registry.svc:5000/openshift/python:latest"


# Define the create_artifact component
@component(name="create_artifact")
def create_artifact(
    input_data: Input[Dataset],
    output_data: Output[Dataset],
    cache_key: Output[str] = None,
    retries: int = 2,
    resource_limits: dict = {"cpu": "1", "memory": "1Gi"},
):
    # Serialize the input data to a pickle file
    with open(input_data.path, "wb") as f:
        pickle.dump(input_data.data, f)

    # Deserialize the pickle file back to a Dataset
    with open(input_data.path, "rb") as f:
        data = pickle.load(f)

    # Store the serialized data in the cache if specified
    if cache_key:
        cache_key = f"{cache_key}_{input_data.name}"
        kfp.components.cache(cache_key, data)

    # Return the serialized data
    return data


# Define the pipeline
@pipeline(
    name="Artifact Pipeline",
    description="Data Serialization and Deserialization using Python's pickle library",
)
def artifact_pipeline():
    # Create an input dataset
    input_dataset = Dataset(type="CSV", path="data.csv")

    # Create an output dataset
    output_dataset = Dataset(type="CSV", path="output.csv")

    # Create an output model
    output_model = Model(type="PyTorch", path="model.pth")

    # Create the create_artifact component
    create_artifact_task = create_artifact(
        input_data=input_dataset,
        output_data=output_dataset,
        cache_key="data_cache",
        retries=2,
        resource_limits={"cpu": "1", "memory": "1Gi"},
    )

    # Add the create_artifact task to the pipeline
    pipeline.add_component(create_artifact_task)

    # Return the pipeline
    return pipeline


# Compile the pipeline
artifact_pipeline.compile()
