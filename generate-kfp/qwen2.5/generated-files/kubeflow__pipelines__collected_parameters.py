
from kfp import dsl

@dsl.pipeline(name="collected_param_pipeline")
def collected_param_pipeline():
    # Define the split_ids component
    split_ids = dsl.component(
        name="split_ids",
        description="Splits a comma-separated string of model IDs into a list of individual IDs.",
        inputs={
            "input_ids": dsl.input("input_ids", type=dsl.StringType())
        },
        outputs={
            "output_ids": dsl.output("output_ids", type=dsl.ListType(dsl.StringType()))
        }
    )

    # Use the split_ids component in the main pipeline
    result = split_ids(input_ids="s1,s2,s3")

    return result
