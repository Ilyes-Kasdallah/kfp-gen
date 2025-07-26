from kfp import pipeline, component

# Import necessary modules
import kfp.dsl as dsl


@dsl.pipeline(name="pipeline-with-after")
def pipeline_with_after():
    # Define the first component
    task1 = component.Component(
        name="task1",
        image="your-custom-image",
        command=["echo", "1st task"],
        outputs=[dsl.Output("output1")],
    )

    # Define the second component
    task2 = component.Component(
        name="task2",
        image="your-custom-image",
        command=["echo", "2nd task"],
        outputs=[dsl.Output("output2")],
    )

    # Define the third component
    task3 = component.Component(
        name="task3",
        image="your-custom-image",
        command=["echo", "3rd task"],
        outputs=[dsl.Output("output3")],
    )

    # Define the after function
    @dsl.after(task1)
    def after_task1():
        print("After task 1 completed")

    # Define the after function
    @dsl.after(task2)
    def after_task2():
        print("After task 2 completed")

    # Define the after function
    @dsl.after(task3)
    def after_task3():
        print("After task 3 completed")


# Run the pipeline
pipeline_with_after()
