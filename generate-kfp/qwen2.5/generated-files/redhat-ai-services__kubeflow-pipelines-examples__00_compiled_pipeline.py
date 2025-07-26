
from kfp import dsl

@dsl.pipeline(name="add_pipeline")
def add_pipeline():
    # Define the first component
    add_component = dsl.component(
        name="add",
        image="image-registry.openshift-image-registry.svc:5000/openshift/python:latest",
        inputs=[
            dsl.input(name="a"),
            dsl.input(name="b")
        ],
        outputs=[
            dsl.output(name="sum")
        ],
        steps=[
            dsl.task(
                name="add",
                python_callable=lambda a, b: a + b,
                inputs=[dsl.input(name="a"), dsl.input(name="b")]
            )
        ]
    )

    # Define the second component
    add_component2 = dsl.component(
        name="add2",
        image="image-registry.openshift-image-registry.svc:5000/openshift/python:latest",
        inputs=[
            dsl.input(name="a"),
            dsl.input(name="b")
        ],
        outputs=[
            dsl.output(name="sum2")
        ],
        steps=[
            dsl.task(
                name="add2",
                python_callable=lambda a, b: a + b,
                inputs=[dsl.input(name="a"), dsl.input(name="b")]
            )
        ]
    )

    # Combine the two components
    return dsl.Combine([add_component, add_component2])

# Function to run the pipeline
def run_pipeline():
    return add_pipeline().run()

# Example usage
if __name__ == "__main__":
    result = run_pipeline()
    print(result)
