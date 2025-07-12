```python
from kfp import dsl

# Define the component with optional inputs
@dsl.component(
    output_artifact=dsl.OutputArtifact(type=dsl.ArtifactType.STRING),
    output_artifact=dsl.OutputArtifact(type=dsl.ArtifactType.BOOLEAN),
    output_artifact=dsl.OutputArtifact(type=dsl.ArtifactType.DICT),
    output_artifact=dsl.OutputArtifact(type=dsl.ArtifactType.LIST),
    output_artifact=dsl.OutputArtifact(type=dsl.ArtifactType.INT)
)
def component_op(
    input_str1: str = 'string default value',
    input_str2: str = None,
    input_str3: str = None,
    input_str4_from_pipeline: str = "Some component default",
    input_str5_from_pipeline: str = "Some pipeline default",
    input_str6_from_pipeline: str = None,
    input_bool1: bool = True,
    input_bool2: bool = None,
    input_dict: dict = {"a": 1},
    input_list: list = ["123"],
    input_int: int = 100
):
    print(f"Input string 1: {input_str1}, Type: {type(input_str1)}")
    print(f"Input string 2: {input_str2}, Type: {type(input_str2)}")
    print(f"Input string 3: {input_str3}, Type: {type(input_str3)}")
    print(f"Input string 4 from pipeline: {input_str4_from_pipeline}, Type: {type(input_str4_from_pipeline)}")
    print(f"Input string 5 from pipeline: {input_str5_from_pipeline}, Type: {type(input_str5_from_pipeline)}")
    print(f"Input string 6 from pipeline: {input_str6_from_pipeline}, Type: {type(input_str6_from_pipeline)}")
    print(f"Input boolean 1: {input_bool1}, Type: {type(input_bool1)}")
    print(f"Input boolean 2: {input_bool2}, Type: {type(input_bool2)}")
    print(f"Input dictionary: {input_dict}, Type: {type(input_dict)}")
    print(f"Input list: {input_list}, Type: {type(input_list)}")
    print(f"Input integer: {input_int}, Type: {type(input_int)}")

# Define the pipeline with optional parameters
@dsl.pipeline(name="v2-component-optional-input")
def component_with_optional_inputs(
    input_str4: str = None,
    input_str5: str = "Some pipeline default",
    input_str6: str = None
):
    component_op(
        input_str4_from_pipeline=input_str4,
        input_str5_from_pipeline=input_str5,
        input_str6_from_pipeline=input_str6
    )

# Execute the pipeline
if __name__ == "__main__":
    kfp.compiler.Compiler().compile(component_with_optional_inputs, "component_with_optional_inputs.yaml")
```

This code snippet defines a Kubeflow Pipeline named `v2-component-optional-input` with a single component `component_op` that accepts various optional inputs. The pipeline also includes optional parameters that can be overridden from the pipeline definition. The pipeline executes the `component_op` with the provided optional parameters.