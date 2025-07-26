import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from baseball_pipeline_branch import CollectStats


@dsl.pipeline(name="Sequential pipeline")
def sequential_pipeline():
    # Define the components
    stats_component = CollectStats()

    # Define the pipeline steps
    step1 = stats_component()
    step2 = stats_component()
    step3 = stats_component()

    # Define the final step
    final_step = stats_component()

    # Return the pipeline
    return final_step


# Example usage of the pipeline
if __name__ == "__main__":
    from kfp import logging

    logging.set_log_level(logging.INFO)
    pipeline.run(sequential_pipeline())
