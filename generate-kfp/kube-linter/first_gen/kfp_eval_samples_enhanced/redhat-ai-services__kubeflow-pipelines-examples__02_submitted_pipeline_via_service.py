from kfp import pipeline
from kfp.dsl import component


@component
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@pipeline(name="add_pipeline")
def add_pipeline():
    """Sequential addition of two numbers."""
    result = add(3.5, 7.2)
    print(f"The sum is: {result}")


# Example usage
if __name__ == "__main__":
    add_pipeline()
