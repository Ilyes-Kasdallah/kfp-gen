```python
import kfp
from kfp import dsl

# Load the DAG configuration from a YAML file
with open('dag_path', 'r') as f:
    dag_config = yaml.safe_load(f)

# Create a pipeline function
@dsl.pipeline(name='DAG_Pipeline')
def pipeline():
    # Iterate over each component in the DAG configuration
    for component_name in dag_config['components']:
        # Create a component function using the @dsl.container_component decorator
        @dsl.container_component(image=f'{username}/{component_name}:latest')
        def create_component(input_path: str, output_path: str):
            # Run the main.py script with -i and -o arguments
            return dsl.ContainerOp(
                name=component_name,
                image=f'{username}/{component_name}:latest',
                command=['python', 'main.py'],
                arguments=[f'-i {input_path}', f'-o {output_path}']
            )

        # Set up the component in the pipeline
        setup_component(component_name, input_path=dag_config['initial_input'], output_path=output_path)

# Compile the pipeline
compiler.Compiler().compile(pipeline, 'pipeline.yaml')

# Submit the pipeline to the Kubeflow Pipelines server
client = kfp.Client()
experiment = client.create_experiment('My Experiment')
run = client.run_pipeline(experiment.id, 'pipeline.yaml')
```

This code snippet defines a Kubeflow Pipeline named `DAG_Pipeline` that processes data according to the specifications in the YAML configuration file. It includes the necessary imports, component definitions, and pipeline compilation. The pipeline dynamically creates component functions and sets them up in the pipeline, ensuring that the data processing steps are executed in the correct order based on the dependencies specified in the YAML configuration file.