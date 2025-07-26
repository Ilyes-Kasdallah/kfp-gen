import pandas as pd
from kfp import components


@dsl.pipeline(name="HypertensionPredictionPipeline")
def hypertension_prediction():
    # Load data from CSV
    load_data = components.load_data(
        source="https://raw.githubusercontent.com/s102401002/kubeflowPipeline0722/main/hypertension_data.csv",
        schema="csv",
    )

    # Define the model
    model = components.Model(
        name="hypothesis_model",
        image="your-model-image",
        entrypoint="your-entrypoint-script",
    )

    # Predict hypertension
    predict_hypertension = components.predict(model=model, input_data=load_data.output)

    # Return the result
    return predict_hypertension.output


# Example usage
if __name__ == "__main__":
    result = hypertension_prediction()
    print(result)
