
from kfp import dsl

@dsl.pipeline(name="baseball-pipeline-enhance")
def baseball_pipeline_enhance():
    # Define the Collect Stats component
    collect_stats_op = dsl.component(
        name="collect_stats_op",
        image="gcr.io/ross-kubeflow/collect-stats:latest",
        inputs={
            "data": dsl.input("data"),
        },
        outputs={
            "stats": dsl.output("stats"),
        },
    )

    # Define the Classification component
    classification_op = dsl.component(
        name="classification_op",
        image="gcr.io/ross-kubeflow/classification:latest",
        inputs={
            "stats": dsl.input("stats"),
        },
        outputs={
            "predictions": dsl.output("predictions"),
        },
    )

    # Define the Pipeline
    return dsl.Pipeline(
        name="baseball-pipeline-enhance",
        steps=[
            collect_stats_op,
            classification_op,
        ],
    )
