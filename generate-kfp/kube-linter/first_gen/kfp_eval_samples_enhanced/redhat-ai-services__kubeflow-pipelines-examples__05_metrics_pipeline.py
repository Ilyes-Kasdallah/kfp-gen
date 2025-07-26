import kfp
from kfp.dsl import pipeline, component


@dsl.pipeline(name="05_metrics_pipeline")
def metrics_pipeline():
    # Define the produce_metrics component
    @component
    def produce_metrics():
        # Generate accuracy-score and mse-score
        accuracy_score = 85
        mse_score = 123456789
        return {"accuracy-score": accuracy_score, "mse-score": mse_score}

    # Main function to execute the pipeline
    @component
    def main():
        # Call the produce_metrics component
        metrics = produce_metrics()
        # Print the generated metrics
        print("Accuracy Score:", metrics["accuracy-score"])
        print("Mean Squared Error:", metrics["mse-score"])


# Execute the pipeline
if __name__ == "__main__":
    metrics_pipeline()
