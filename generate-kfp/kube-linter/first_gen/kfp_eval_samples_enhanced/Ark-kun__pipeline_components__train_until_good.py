import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from ark_kun.pipeline_components import train_model, evaluate_model


@pipeline(name="train_until_low_error")
def train_until_low_error():
    # Define the training component
    train_model_component = train_model()

    # Define the evaluation component
    evaluate_model_component = evaluate_model()

    # Define the main loop to train until a satisfactory error threshold is reached
    @component
    def train_until_good():
        # Call the training component
        result = train_model_component()

        # Call the evaluation component
        evaluation_result = evaluate_model_component(result)

        # Check if the evaluation result is satisfactory
        if evaluation_result < 0.01:
            # If not, call the training component again
            return train_until_good()
        else:
            # If satisfactory, return the result
            return result


# Example usage
if __name__ == "__main__":
    train_until_good()
