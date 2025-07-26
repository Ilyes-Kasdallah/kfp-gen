
from kfp import dsl

@dsl.pipeline(name="metrics_visualization_pipeline")
def metrics_visualization_pipeline():
    # Define the components
    wine_classification = dsl.component(
        name="wine-classification",
        description="Perform wine classification.",
        inputs={
            "data": dsl.input("data", type=dsl.InputType.PATH)
        },
        outputs={
            "metrics": dsl.output("metrics", type=dsl.OutputType.METRICS)
        }
    )

    # Define the test function
    metrics_visualization_v2_test = dsl.component(
        name="metrics_visualization_v2_test",
        description="Test the metrics_visualization_pipeline function.",
        inputs={
            "input_data": dsl.input("input_data", type=dsl.InputType.PATH)
        },
        outputs={
            "result": dsl.output("result", type=dsl.OutputType.STRING)
        }
    )

    # Define the main function
    @dsl.function(name="main")
    def main():
        # Call the wine_classification component
        metrics = wine_classification(input_data="path/to/wine_data.csv")

        # Call the metrics_visualization_v2_test component
        result = metrics_visualization_v2_test(input_data="path/to/input_data.csv")

        # Print the result
        print(result)

# Run the pipeline
if __name__ == "__main__":
    main()
