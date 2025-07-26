import kfp
from kfp.dsl import pipeline, component

# Define the pipeline function name
pipeline_name = "Kubeflow Fairing Pipeline"

# Define the component function name
lightgbm_training = component("lightgbm_training")

# Define the training data and parameters
training_data = {
    "train_file": "path/to/train/data.csv",
    "test_file": "path/to/test/data.csv",
    "num_boost_rounds": 100,
    "objective": "binary:logistic",
    "learning_rate": 0.05,
    "max_depth": 6,
    "min_samples_split": 2,
    "min_samples_leaf": 1,
    "feature_fraction": 0.75,
    "bagging_fraction": 0.8,
    "colsample_bytree": 0.9,
    "subsample": 0.8,
    "n_estimators": 1000,
    "verbose": 1,
}


# Define the pipeline
@pipeline(name=pipeline_name)
def run_lightgbm_training():
    # Use the lightgbm_training component to train the model
    trained_model = lightgbm_training(training_data)

    # Return the trained model
    return trained_model


# Example usage
if __name__ == "__main__":
    # Run the pipeline
    result = run_lightgbm_training()
    print(result)
