
from kfp import dsl

@dsl.pipeline(name="pipeline-with-after")
def pipeline_with_after():
    # Task 1: Print Text
    task1 = dsl.component(
        name="Print Text",
        image="alpine:latest",
        command=["echo", "1st task"],
    )

    # Task 2: Print Text
    task2 = dsl.component(
        name="Print Text",
        image="alpine:latest",
        command=["echo", "2nd task"],
    )

    # Task 3: Print Text
    task3 = dsl.component(
        name="Print Text",
        image="alpine:latest",
        command=["echo", "3rd task"],
    )

    # After the first task, print the result of the second task
    task1.after(task2)

    # After the second task, print the result of the third task
    task2.after(task3)

# Run the pipeline
pipeline_with_after()
