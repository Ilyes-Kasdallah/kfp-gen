
from kfp import pipeline
from kfp.dsl import component

@dsl.pipeline(name='ml-demo')
def ml_demo():
    # Define the first component
    @component
    def model_training():
        # Simulate model training
        print("Model training started...")
        return "Model trained successfully"

    # Define the second component
    @component
    def model_inference():
        # Simulate model inference
        print("Model inference started...")
        return "Model inference successful"

    # Define the third component
    @component
    def model_prediction():
        # Simulate model prediction
        print("Model prediction started...")
        return "Model prediction successful"

    # Execute the pipeline
    ml_training = model_training()
    ml_inference = model_inference()
    ml_prediction = model_prediction()

    # Print the results
    print(ml_training)
    print(ml_inference)
    print(ml_prediction)

# Run the pipeline
ml_demo()
