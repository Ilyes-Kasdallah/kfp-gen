
from kfp import pipeline
from kfp.components import CollectStats

@pipeline(name="Sequential pipeline")
def sequential_pipeline():
    # Define the components
    stats_component = CollectStats()
    
    # Define the pipeline steps
    step1 = stats_component()
    step2 = stats_component()
    step3 = stats_component()
    
    # Return the pipeline
    return step1, step2, step3

# Example usage
if __name__ == "__main__":
    pipeline.run(sequential_pipeline())
