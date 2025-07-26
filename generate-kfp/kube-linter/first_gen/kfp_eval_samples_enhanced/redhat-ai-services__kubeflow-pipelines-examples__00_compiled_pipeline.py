from kfp import pipeline
from kfp.dsl import component


@component
def add(a: float, b: float) -> float:
    """Add two floats."""
    return a + b


@pipeline(name="add_pipeline")
def add_pipeline():
    """Add two floats."""
    # First addition
    result1 = add(3.5, 2.0)

    # Second addition
    result2 = add(result1, 4.0)

    return result2


# Example usage
if __name__ == "__main__":
    add_pipeline()
