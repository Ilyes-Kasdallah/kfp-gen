
from kfp import pipeline
from kfp.components import component

@dsl.pipeline(name="convert_kedro_pipeline_to_kfp")
def convert_kedro_pipeline_to_kfp(pipelines):
    # Define the pipeline function name
    pod_per_node_pipeline_generator = "pod_per_node_pipeline_generator"
    
    # Iterate over each node in the input Kedro pipeline
    for node in pipelines[pipeline].node_dependencies:
        # Create a component for each node
        component_name = f"{pod_per_node_pipeline_generator}_{node}"
        component = component(
            name=component_name,
            inputs=pipelines[pipeline].inputs[node],
            outputs=pipelines[pipeline].outputs[node]
        )
        
        # Add the component to the pipeline
        yield component

# Example usage
pipeline = {
    "name": "example_pipeline",
    "node_dependencies": {
        "feature_engineering": ["data_preprocessing", "model_training"],
        "data_preprocessing": ["feature_selection", "data_normalization"],
        "model_training": ["feature_selection", "model_selection"]
    }
}

convert_kedro_pipeline_to_kfp(pipeline)
