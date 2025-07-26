
from kfp import dsl

@dsl.pipeline(name="MyKubeflowPipeline")
def MyKubeflowPipeline():
    # Define the dataset
    dataset = dsl.Dataset("my_dataset", description="A sample dataset for training a model")

    # Define the model
    model = dsl.Model(
        name="my_model",
        description="A simple machine learning model",
        source="https://huggingface.co/models/transformers/stable-mlp",
        version="0.7.0",
        tags=["transformers"],
    )

    # Define the training pipeline
    training_pipeline = dsl.Pipeline(
        name="TrainingPipeline",
        steps=[
            dsl.InputDataset(dataset),
            dsl.Model(model),
            dsl.TrainModel(
                model=model,
                input_dataset=dataset,
                output_dir="output_dir",
                batch_size=32,
                epochs=5,
                logging_mode="off",
            ),
        ],
    )

    return training_pipeline
