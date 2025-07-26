
from kfp import dsl

@dsl.pipeline(name="pipeline-with-after")
def pipeline_with_after():
    # Task 1: Print "1st task"
    task1 = dsl.component(
        name="task1",
        image="your-custom-container-image",
        command=["echo", "1st task"],
        outputs={"stdout": dsl.output("stdout")},
    )

    # Task 2: Print "2nd task"
    task2 = dsl.component(
        name="task2",
        image="your-custom-container-image",
        command=["echo", "2nd task"],
        outputs={"stdout": dsl.output("stdout")},
    )

    # Task 3: Print "3rd task"
    task3 = dsl.component(
        name="task3",
        image="your-custom-container-image",
        command=["echo", "3rd task"],
        outputs={"stdout": dsl.output("stdout")},
    )

    # After the first two tasks, print "After first two tasks"
    after_task1 = dsl.after(task1, task2)

    # After the third task, print "After third task"
    after_task3 = dsl.after(task3, task2)

    # The final output of the pipeline
    final_output = dsl.output("final_output")

    # The pipeline execution
    return dsl.Pipeline(
        name="pipeline-with-after",
        steps=[
            task1,
            after_task1,
            task2,
            after_task2,
            task3,
            after_task3,
            final_output,
        ],
    )
