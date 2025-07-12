```python
from kfp import dsl

# Define the pipeline
@dsl.pipeline(name='v2-container-component-no-input')
def pipeline_container_no_input():
    # Define the component
    @dsl.component(
        base_image='python:3.7',
        packages_to_install=[''],
        executor_spec=dsl.ExecutorSpec(
            machine_type='n1-standard-4'
        )
    )
    def container_no_input():
        # Execute a simple echo command
        print("hello world")

# Run the pipeline
if __name__ == '__main__':
    from kfp.compiler import.Compiler
    compiler = Compiler()
    pipeline_package_path = compiler.compile(pipeline_container_no_input, package_path='pipeline_container_no_input.tar.gz')
    print(f"Pipeline package path: {pipeline_package_path}")
```

This code snippet defines a Kubeflow Pipeline named `v2-container-component-no-input` with a single component `container_no_input`. The component runs a simple `echo "hello world"` command using a Docker image `python:3.7`. The pipeline is executed by compiling it into a tar.gz file and running it using the `Compiler` class from the `kfp.compiler` module.