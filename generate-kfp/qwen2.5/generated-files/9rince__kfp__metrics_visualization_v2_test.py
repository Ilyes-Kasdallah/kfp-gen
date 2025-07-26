
from kfp import dsl

@dsl.pipeline(name="metrics_visualization_pipeline")
def metrics_visualization_pipeline():
    # Define the components
    wine_classification = dsl.component(
        name="wine-classification",
        description="Perform a wine classification task.",
        inputs={
            "data": dsl.input("data", type="string"),
        },
        outputs={
            "metrics": dsl.output("metrics", type="dict"),
        },
    )

    # Define the test function
    metrics_visualization_v2_test = dsl.component(
        name="metrics_visualization_v2_test",
        description="Test the metrics_visualization_pipeline function.",
        inputs={
            "input_data": dsl.input("input_data", type="string"),
        },
        outputs={
            "result": dsl.output("result", type="dict"),
        },
    )

    # Define the main function
    @dsl.function(name="main")
    def main(input_data):
        # Perform the wine classification task
        classification_metrics = wine_classification(input_data)
        
        # Test the metrics_visualization_pipeline function
        result = metrics_visualization_v2_test(input_data)
        
        return {
            "classification_metrics": classification_metrics,
            "result": result,
        }

# Example usage
if __name__ == "__main__":
    main("your_input_data_here")
