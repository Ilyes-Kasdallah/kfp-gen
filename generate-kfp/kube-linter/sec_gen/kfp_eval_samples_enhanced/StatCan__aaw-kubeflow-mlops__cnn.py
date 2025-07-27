import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@dsl.pipeline(name="Tacos vs. Burritos")
def tacos_vs_burritos():
    # Define the CNN component
    @component
    def cnn(input_dataset: Dataset, output_model: Model):
        # Load the input dataset
        data = input_dataset.read_csv()

        # Define the CNN model
        model = Model(
            name="tacos_vs_burritos",
            image="tensorflow/tensorflow:latest",
            input_columns=["feature1", "feature2"],
            output_columns=["prediction"],
        )

        # Train the model
        model.fit(data)

        # Save the trained model
        model.save(output_model)

    # Define the exit handler component
    @component
    def exit_handler(callback_url: str):
        # Send a completion message to the callback URL
        curl_command = f"curl -X POST -H 'Content-Type: application/json' -d '{callback_url}' http://kubemlopsbot-svc.kubeflow.svc.cluster.local:8080"
        print(curl_command)
        return None


# Run the pipeline
tacos_vs_burritos()
