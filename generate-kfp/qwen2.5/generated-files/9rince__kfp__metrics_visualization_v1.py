
from kfp import dsl

@dsl.pipeline(name="metrics-visualization-v1-pipeline")
def metrics_visualization_v1():
    # Define the components
    confusion_visualization = dsl.component(
        name="confusion_visualization",
        description="Generates a confusion matrix visualization.",
        inputs={
            "data": dsl.input(type="array", items=dsl.input(type="string"))
        },
        outputs={
            "confusion_matrix": dsl.output(type="array", items=dsl.output(type="string"))
        }
    )

    # Execute the components
    confusion_visualization(data=["class1", "class2", "class3", "class4", "class5"])
