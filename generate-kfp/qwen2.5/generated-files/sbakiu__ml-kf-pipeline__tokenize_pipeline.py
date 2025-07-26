
from kfp import dsl

@dsl.pipeline(name="Pipeline")
def Pipeline():
    # Define the input file
    reddit_train = dsl.Input("reddit_train.csv")

    # Define the tokenize component
    tokenize_pipeline = dsl.component(
        name="tokenize_pipeline",
        steps=[
            dsl.pipeline_step(
                name="tokenize",
                python_script="src.steps.tokenize.pipeline_step",
                inputs={"input": reddit_train},
                outputs={"output": "tokenized_data"}
            )
        ]
    )

    # Return the tokenize component
    return tokenize_pipeline
