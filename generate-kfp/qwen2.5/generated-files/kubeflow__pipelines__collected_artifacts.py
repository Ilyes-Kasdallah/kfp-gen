
from kfp import dsl

@dsl.pipeline(name="collecting_artifacts")
def collecting_artifacts(model_ids):
    """
    This pipeline takes a comma-separated string of model IDs and returns a list of individual IDs.
    """
    # Split the input string into a list of model IDs
    model_ids_list = model_ids.split(',')
    
    # Return the list of model IDs
    return model_ids_list
