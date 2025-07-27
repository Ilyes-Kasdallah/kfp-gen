import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the component with optional inputs
@component_with_optional_inputs
def component_op(
    input_string: str = None,
    input_boolean: bool = None,
    input_dict: dict = None,
    input_list: list = None,
    input_integer: int = None,
):
    # Perform some operation based on the input parameters
    result = input_string + input_boolean + input_dict + input_list + input_integer
    return result


# Define the pipeline
pipeline_root = "gs://my-bucket/pipeline-root"
pipeline = pipeline(
    name="v2-component-optional-input",
    steps=[
        component_op(
            input_string="Hello",
            input_boolean=True,
            input_dict={"key": "value"},
            input_list=[1, 2, 3],
            input_integer=4,
        ),
    ],
)

# Compile the pipeline
compiler = kfp.compiler.Compiler()
compiled_pipeline = compiler.compile(pipeline)
print(compiled_pipeline)
