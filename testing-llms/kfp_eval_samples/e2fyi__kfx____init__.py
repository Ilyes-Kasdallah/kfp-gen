```python
from kfp import dsl
from kfx import ContainerOpTransform, ArtifactLocationHelper

# Define the echo component
@dsl.component(
    base_image="ubuntu",
    packages_to_install=["matplotlib", "vega-lite"],
    container_op_transform=ContainerOpTransform(
        resources={"requests": {"cpu": "100m"}, "limits": {"cpu": "500m"}},
        image_pull_policy="IfNotPresent",
        env_vars={
            "DISPLAY": ":99"
        }
    )
)
def echo(text: str) -> str:
    print(text)
    return text

# Define the test_op component
@dsl.component(
    base_image="ubuntu",
    packages_to_install=["matplotlib", "vega-lite"],
    container_op_transform=ContainerOpTransform(
        resources={"requests": {"cpu": "100m"}, "limits": {"cpu": "500m"}},
        image_pull_policy="IfNotPresent",
        env_vars={
            "DISPLAY": ":99"
        }
    )
)
def test_op() -> dsl.Artifact:
    # Create a simple bar chart visualization
    import matplotlib.pyplot as plt
    import json
    
    x = ["A", "B", "C"]
    y = [10, 20, 30]
    
    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.set_title("Sample Bar Chart")
    ax.set_xlabel("Categories")
    ax.set_ylabel("Values")
    
    # Convert the plot to JSON format
    plot_json = json.dumps(fig.to_dict())
    
    # Write the JSON to a file
    with open("bar_chart.json", "w") as f:
        f.write(plot_json)
    
    # Return the markdown data
    markdown_data = """
    ```json
    {plot_json}
    ```
    """.format(plot_json=plot_json)
    
    return dsl.Artifact(type=dsl.ArtifactType.TEXT, uri="gs://your-bucket/path/to/bar_chart.md", description="Markdown data for the bar chart visualization")

# Define the main pipeline
@dsl.pipeline(name="demo")
def demo():
    # First echo operation
    first_echo = echo(text="Hello, World!")
    
    # Second echo operation using the output of the first echo operation
    second_echo = echo(text=first_echo.outputs.text)
    
    # Test operation
    test_result = test_op()

# Compile the pipeline
compiler.Compiler().compile(demo, __name__)
```

This code defines a Kubeflow Pipeline named `demo` that includes two components: `echo` and `test_op`. The `echo` component prints a given string to the standard output and returns the same string. The `test_op` component generates a simple bar chart visualization using Vega-Lite and writes markdown text to an output file. The pipeline runs these operations sequentially, with the second `echo` operation occurring after the first. The `test_op` component's output will be displayed in the Kubeflow UI based on the metadata generated.