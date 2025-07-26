from kfp import pipeline
from kfp.dsl import component


@component
def print_op(message):
    """Prints a given message to the standard output."""
    print(message)
    return message


@pipeline(name="loop_with_after_dependency_set")
def loop_with_after_dependency_set():
    """A pipeline that demonstrates parallel execution and dependency management."""
    # First component: Print "Hello, World!"
    print_op("Hello, World!")

    # Second component: Print "This is the second component."
    print_op("This is the second component.")

    # Third component: Print "This is the third component."
    print_op("This is the third component.")

    # Parallel execution with after dependency set
    parallel_after_dependency_set = [
        print_op("Parallel operation 1"),
        print_op("Parallel operation 2"),
        print_op("Parallel operation 3"),
    ]

    # Execute the pipeline
    parallel_after_dependency_set[0].execute()
    parallel_after_dependency_set[1].execute()
    parallel_after_dependency_set[2].execute()


# Run the pipeline
loop_with_after_dependency_set()
