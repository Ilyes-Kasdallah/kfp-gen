```python
import kfp
from kfp import dsl

# Define the components
@dsl.component(
    base_image="python:3.8",
    packages_to_install=["numpy"],
    enable_caching=False,
)
def split_ids(input_ids: str) -> list[str]:
    return input_ids.split(",")

@dsl.component(
    base_image="python:3.8",
    packages_to_install=["numpy"],
    enable_caching=False,
)
def prepend_id(model_id: str) -> str:
    return f"model_id_{model_id}"

@dsl.component(
    base_image="python:3.8",
    packages_to_install=["numpy"],
    enable_caching=False,
)
def consume_single_id(model_id: str) -> str:
    print(f"Consuming {model_id}")
    return "completed"

@dsl.component(
    base_image="python:3.8",
    packages_to_install=["numpy"],
    enable_caching=False,
)
def consume_ids(model_ids: list[str]) -> str:
    for model_id in model_ids:
        consume_single_id(model_id)
    return "completed"

# Define the collecting_parameters sub-pipeline
@dsl.pipeline(name="collecting_parameters")
def collecting_parameters(initial_input_ids: str):
    ids = split_ids(initial_input_ids)
    for id in dsl.ParallelFor(ids):
        prepend_id(id)
        consume_single_id(prepend_id(id))

# Define the main pipeline
@dsl.pipeline(name="collected_param_pipeline")
def collected_param_pipeline():
    collecting_parameters("s1,s2,s3")
    consume_ids(collecting_parameters.outputs["ids"])

# Compile the pipeline
compiler = kfp.compiler.Compiler()
pipeline_spec = compiler.compile(collected_param_pipeline, package_path="collected_parameters.yaml")

# Submit the pipeline
client = kfp.Client()
experiment = client.create_experiment("Collected Parameters Experiment")
run = client.run(experiment.id, pipeline_spec=pipeline_spec)
```

This code defines the required components and the pipeline structure as described in the question. It includes the necessary imports, component definitions, and the pipeline orchestration logic. The pipeline is compiled and submitted to the Kubeflow Pipelines server.