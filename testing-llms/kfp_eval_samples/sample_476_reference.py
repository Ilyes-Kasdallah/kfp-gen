from kfp import dsl
from kfp import compiler
from kfp import Client

# One component used in a simple pipeline. Compiles pipeline to YAML and creates 
# a run from the pipeline YAML.

@dsl.component
def say_hello(name: str) -> str:
    hello_text = f"Hello, {name}!"
    print(hello_text)
    return hello_text


@dsl.pipeline
def hello_pipeline(recipient: str) -> str:
    hello_task = say_hello(name=recipient)
    return hello_task.output


def compile(pipeline_name: str):
    compiler.Compiler().compile(hello_pipeline, pipeline_name)


def run(endpoint: str, pipeline_name: str) -> str:
    client = Client(host=endpoint)
    run = client.create_run_from_pipeline_package(
        pipeline_name, 
        arguments={
            "recipient": "World",
        },
    )
    url = f"{endpoint}/#/runs/details/{run.run_id}"
    return url


def main():
    pipeline_name = "pipeline.yaml"
    endpoint = "http://localhost:8080"
    compile(pipeline_name)
    url = run(endpoint, pipeline_name)
    print(url)


if __name__ == "__main__":
    main()
