
from kubeflow.pipelines import test_pod_per_node_pipeline_generator

@dsl.pipeline(name="pipeline")
def pipeline():
    # Define components
    data_processing_component = test_pod_per_node_pipeline_generator()
    
    # Define pipeline steps
    data_processing_component.run()
    data_processing_component.wait_for_completion()

# Run the pipeline
pipeline()
