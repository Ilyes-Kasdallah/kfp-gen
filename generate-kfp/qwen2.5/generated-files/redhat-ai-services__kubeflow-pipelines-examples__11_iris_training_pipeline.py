
from kfp import dsl

@dsl.pipeline(name="11_iris_training_pipeline")
def iris_training_pipeline():
    # Load the Iris dataset
    data = dsl.input_dataset("iris_data")
    
    # Split the dataset into training and testing sets
    train, test = dsl.split_dataset(data, test_size=0.3)
    
    # Define the model
    model = dsl.component(
        name="iris_model",
        inputs={
            "X": train,
            "y": test
        },
        outputs={
            "model": dsl.output_artifact("iris_model")
        }
    )
    
    # Train the model
    model.train()
    
    # Evaluate the model
    model.evaluate()
    
    # Save the trained model
    model.save()

# Example usage
iris_training_pipeline()
