
from kfp import dsl

@dsl.pipeline(name="simple-training-pipeline")
def simple_training_pipeline(
    model_type="resnet",
    # Add more parameters as needed
):
    # Define the training component
    training_component = dsl.component(
        name="training",
        description="Training a machine learning model.",
        inputs={
            "model_type": dsl.Input(type="string", default="resnet"),
            # Add more inputs as needed
        },
        outputs={
            "model": dsl.Output(type="object"),
            # Add more outputs as needed
        },
        steps=[
            dsl.task(
                name="train_model",
                description="Train the specified model.",
                inputs={
                    "model_type": dsl.Input(type="string", default="resnet"),
                    # Add more inputs as needed
                },
                outputs={
                    "model": dsl.Output(type="object"),
                    # Add more outputs as needed
                },
                steps=[
                    dsl.python_step(
                        name="train_model",
                        python_code=f"""
                            from tensorflow.keras.models import load_model
                            from tensorflow.keras.preprocessing.image import ImageDataGenerator
                            from sklearn.model_selection import train_test_split

                            model = load_model('{model_type}')
                            data_generator = ImageDataGenerator(rescale=1./255)
                            train_datagen = data_generator.flow_from_directory('path/to/train', target_size=(224, 224), batch_size=32)

                            validation_datagen = data_generator.flow_from_directory('path/to/validation', target_size=(224, 224), batch_size=32)

                            model.fit(train_datagen, validation_data=validation_datagen, epochs=10)
                        """,
                        language="python"
                    )
                ]
            )
        ]
    )

    return training_component
