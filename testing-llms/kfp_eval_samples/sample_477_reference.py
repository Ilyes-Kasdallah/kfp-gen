from kfp import dsl
from kfp import Client

# Simple pipeline that chains to invocations of a single component to each
# other. Does not produce KFP IR through compilation and instead creates a run
# directly from the pipeline function defined here.

@dsl.component
def addition_component(num1: int, num2: int) -> int:
    return num1 + num2

@dsl.pipeline(name='addition-pipeline')
def my_pipeline(a: int, b: int, c: int = 10):
    add_task_1 = addition_component(num1=a, num2=b)
    add_task_2 = addition_component(num1=add_task_1.output, num2=c)

def run(endpoint: str, pipeline) -> str:
    client = Client(host=endpoint)
    run = client.create_run_from_pipeline_func(
        pipeline, 
        arguments={
            "a": 1,
            "b": 2
        },
    )
    url = f"{endpoint}/#/runs/details/{run.run_id}"
    return url

def main():
    endpoint = "http://localhost:8080"
    pipeline = my_pipeline
    url = run(endpoint, pipeline)
    print(url)

if __name__ == "__main__":
    main()