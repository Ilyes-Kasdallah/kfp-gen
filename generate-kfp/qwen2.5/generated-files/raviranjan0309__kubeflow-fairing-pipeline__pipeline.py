
from kfp import pipeline
from kfp.components import component

@component
def lightgbm_training(
    input_data,
    num_rounds=10,
    learning_rate=0.05,
    max_depth=7,
    min_samples_split=2,
    min_samples_leaf=1,
    n_estimators=100,
    random_state=42,
):
    # Define the training pipeline
    return {
        "inputs": {
            "input_data": input_data,
        },
        "outputs": {
            "model": {
                "type": "ml.model",
                "version": "1.0",
            },
        },
        "steps": [
            {
                "name": "train",
                "image": "gcr.io/<GCP PROJECT ID>/lightgbm-model:latest",
                "command": [
                    "python",
                    "train.py",
                    "--input-data",
                    input_data,
                    "--num-iterations",
                    num_rounds,
                    "--learning-rate",
                    learning_rate,
                    "--max-depth",
                    max_depth,
                    "--min-sample-split",
                    min_samples_split,
                    "--min-sample-leaf",
                    min_samples_leaf,
                    "--n_estimators",
                    n_estimators,
                    "--random-state",
                    random_state,
                ],
            },
        ],
    }

@pipeline(name="Kubeflow Fairing Pipeline")
def create_kubeflow_fairing_pipeline():
    return lightgbm_training()

# Example usage
if __name__ == "__main__":
    pipeline.run(create_kubeflow_fairing_pipeline())
