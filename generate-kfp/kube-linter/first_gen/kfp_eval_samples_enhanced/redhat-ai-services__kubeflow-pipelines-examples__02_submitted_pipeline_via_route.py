from kfp import pipeline, component
from kfp.dsl import Input, Output


@component
def add(a: float, b: float) -> float:
    """Add two floats."""
    return a + b


@pipeline(name="add_pipeline")
def add_pipeline():
    """Add two floats."""
    a = Input("a", float)
    b = Input("b", float)
    result = add(a, b)
    Output("result", float)


# Example usage
if __name__ == "__main__":
    add_pipeline().run()
