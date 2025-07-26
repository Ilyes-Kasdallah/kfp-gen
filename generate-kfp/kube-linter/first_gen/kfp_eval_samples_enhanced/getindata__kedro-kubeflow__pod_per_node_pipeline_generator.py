import kfp
from kfp.dsl import component, pipeline


@dsl.pipeline(name="convert_kedro_pipeline_to_kfp")
def pod_per_node_pipeline_generator(pipelines):
    # Define the pipeline components
    components = []
    for node_name, dependencies in pipelines.items():
        # Create a component for each node
        component = component(
            name=f"{node_name}_component",
            description=f"Convert {node_name} to KFP container",
            inputs=dependencies,
            outputs=kfp.outputs.KFPContainer(),
        )
        components.append(component)

    # Return the pipeline components
    return components


# Example usage
pipeline_definition = pod_per_node_pipeline_generator(pipelines)
