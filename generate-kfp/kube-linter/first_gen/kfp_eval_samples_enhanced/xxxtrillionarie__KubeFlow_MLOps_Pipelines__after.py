from kfp import pipeline, component


@dsl.pipeline(name="pipeline-with-after")
def pipeline_with_after():
    # Define the first component
    task1 = component.Component(
        name="Print Text",
        image="alpine:latest",
        steps=[
            component.Step(
                name="Print Text",
                code="print('1st task')",
                outputs={"stdout": {"path": "/dev/stdout"}},
            )
        ],
    )

    # Define the second component
    task2 = component.Component(
        name="Print Text",
        image="alpine:latest",
        steps=[
            component.Step(
                name="Print Text",
                code="print('2nd task')",
                outputs={"stdout": {"path": "/dev/stdout"}},
            )
        ],
    )

    # Define the third component
    task3 = component.Component(
        name="Print Text",
        image="alpine:latest",
        steps=[
            component.Step(
                name="Print Text",
                code="print('3rd task')",
                outputs={"stdout": {"path": "/dev/stdout"}},
            )
        ],
    )

    # Use after as the pipeline function name
    return task1.after(task2.after(task3))


# Example usage
if __name__ == "__main__":
    pipeline_with_after().run()
