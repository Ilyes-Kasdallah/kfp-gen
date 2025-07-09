from types import FunctionType

from kfp.compiler import Compiler
from kfp import dsl
import kfp.components as comp


@dsl.pipeline(
    name="Test",
    description="test",
)
def pipeline():
    c:FunctionType = comp.load_component_from_file("./components/task1/component.yaml")

    task1 = c(
        input_path="hogehoge/fugafuga",
    )

    c(
        input_path=task1.outputs["output_path"],
    )

def main():
    Compiler().compile(
        pipeline_func=pipeline,
        package_path="./pipeline.yaml",
    )

if __name__ == "__main__":
    main()
