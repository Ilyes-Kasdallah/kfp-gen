
from kfp import dsl

@dsl.pipeline(name="loop_with_after_dependency_set")
def loop_with_after_dependency_set():
    # Define the first component: print_op
    print_op = dsl.component(
        name="print_op",
        description="Prints a message to the standard output.",
        steps=[
            dsl.output("output", description="The output of print_op."),
            dsl.step(
                name="step1",
                description="First step of the pipeline.",
                operations=[dsl.print_op("Hello, World!")]
            ),
            dsl.step(
                name="step2",
                description="Second step of the pipeline.",
                operations=[dsl.print_op("Hello, Again!")]
            ),
            dsl.step(
                name="step3",
                description="Third step of the pipeline.",
                operations=[dsl.print_op("Hello, Third!")]
            )
        ]
    )

    # Define the second component: parallel_after_dependency
    parallel_after_dependency = dsl.component(
        name="parallel_after_dependency",
        description="Parallelizes the execution of the first two components.",
        steps=[
            dsl.parallel(
                name="parallel_step1",
                description="Parallel step 1 of the pipeline.",
                operations=[dsl.print_op("Hello, World!"), print_op("Hello, Again!")]
            ),
            dsl.parallel(
                name="parallel_step2",
                description="Parallel step 2 of the pipeline.",
                operations=[dsl.print_op("Hello, Third!"), print_op("Hello, Fourth!")]
            )
        ]
    )

    # Use parallel_after_dependency as the pipeline function name
    return parallel_after_dependency
