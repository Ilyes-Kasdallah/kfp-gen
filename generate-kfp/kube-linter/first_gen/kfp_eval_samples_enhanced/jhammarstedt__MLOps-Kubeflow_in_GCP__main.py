import kfp
from kfp.dsl import component, pipeline


@dsl.pipeline(name="ml-demo")
def ml_demo():
    # Define the first component
    @component
    def model_training():
        # Implement the logic for model training
        print("Model training started...")
        return "Model trained successfully"

    # Define the second component
    @component
    def model_evaluation():
        # Implement the logic for model evaluation
        print("Model evaluation started...")
        return "Model evaluation successful"

    # Define the third component
    @component
    def model_prediction():
        # Implement the logic for model prediction
        print("Model prediction started...")
        return "Model prediction successful"

    # Execute the pipeline
    ml_demo()
