
from kfp import dsl

@dsl.pipeline(name="test-run-local-pipeline")
def test_run_local_pipeline():
    hello = dsl.component(
        name="hello",
        python_callable=lambda name: f"hello {name}",
    )

    # Define the pipeline steps
    step1 = hello(name="Alice")
    step2 = hello(name="Bob")
    step3 = hello(name="Charlie")
    step4 = hello(name="David")
    step5 = hello(name="Eve")
    step6 = hello(name="Frank")

    # Combine the steps into a single pipeline function
    local_client_test = dsl.PipelineFunction(
        name="local_client_test",
        steps=[step1, step2, step3, step4, step5, step6],
    )

# Run the pipeline
local_client_test()
