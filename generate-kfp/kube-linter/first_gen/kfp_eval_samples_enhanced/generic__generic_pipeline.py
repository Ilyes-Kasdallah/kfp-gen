from kfp import dsl


@dsl.pipeline(name="Generic Pipeline")
def generic_pipeline():
    # Define components
    component1 = dsl.component(
        name="Component 1",
        description="This is the first component of the pipeline.",
        inputs={"input1": dsl.Input(type="string"), "input2": dsl.Input(type="int")},
        outputs={
            "output1": dsl.Output(type="string"),
            "output2": dsl.Output(type="int"),
        },
    )

    component2 = dsl.component(
        name="Component 2",
        description="This is the second component of the pipeline.",
        inputs={"input3": dsl.Input(type="float"), "input4": dsl.Input(type="bool")},
        outputs={
            "output3": dsl.Output(type="float"),
            "output4": dsl.Output(type="bool"),
        },
    )

    # Define the pipeline
    return dsl.Pipeline(name="Generic Pipeline", steps=[component1, component2])
