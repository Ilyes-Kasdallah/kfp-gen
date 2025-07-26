
from kfp import workflow

@workflow(name="A Simple CI Pipeline")
def simple_ci_pipeline():
    # Define the first component: add_op
    add_op = workflow.PipelineOp(
        name="add_op",
        description="Add two integers",
        steps=[
            workflow.PipelineOp(
                name="step1",
                description="Add x_value and y_value",
                steps=[
                    workflow.PipelineOp(
                        name="step2",
                        description="Calculate the sum",
                        steps=[
                            workflow.PipelineOp(
                                name="step3",
                                description="Output the result",
                                outputs={
                                    "sum": "result"
                                }
                            )
                        ]
                    )
                ]
            )
        ]
    )

    # Define the second component: multiply_op
    multiply_op = workflow.PipelineOp(
        name="multiply_op",
        description="Multiply two integers",
        steps=[
            workflow.PipelineOp(
                name="step1",
                description="Multiply x_value and y_value",
                steps=[
                    workflow.PipelineOp(
                        name="step2",
                        description="Calculate the product",
                        steps=[
                            workflow.PipelineOp(
                                name="step3",
                                description="Output the result",
                                outputs={
                                    "product": "result"
                                }
                            )
                        ]
                    )
                ]
            )
        ]
    )

    # Define the third component: divide_op
    divide_op = workflow.PipelineOp(
        name="divide_op",
        description="Divide two integers",
        steps=[
            workflow.PipelineOp(
                name="step1",
                description="Divide x_value by y_value",
                steps=[
                    workflow.PipelineOp(
                        name="step2",
                        description="Calculate the quotient",
                        steps=[
                            workflow.PipelineOp(
                                name="step3",
                                description="Output the result",
                                outputs={
                                    "quotient": "result"
                                }
                            )
                        ]
                    )
                ]
            )
        ]
    )

    # Call the components in the pipeline
    add_op()
    multiply_op()
    divide_op()

# Execute the pipeline
simple_ci_pipeline()
