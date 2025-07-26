import kfp
from kfp.dsl import component, pipeline


@component
def _python_op(x):
    # Placeholder for the actual Python operation
    return x * 2


@pipeline(name="pipeline_from_func")
def pipeline_from_func():
    # Define the pipeline steps
    step1 = component(
        name="step1",
        python_op=_python_op,
        inputs={"input": kfp.dsl.Input()},
        outputs={"output": kfp.dsl.Output()},
    )

    step2 = component(
        name="step2",
        python_op=_python_op,
        inputs={"input": kfp.dsl.Input()},
        outputs={"output": kfp.dsl.Output()},
    )

    # Combine the steps into a single pipeline
    return step1 + step2


# Example usage
if __name__ == "__main__":
    pipeline_from_func().execute()
