```python
import kfp
from kfp import dsl

# Import necessary libraries
import subprocess

# Define the Flip Coin component
@dsl.component(
    base_image="python:3.8",
    packages_to_install=["numpy"],
)
def flip_coin():
    # Simulate a coin flip
    result = subprocess.run(["sh", "-c", "echo $(openssl rand -hex 1 | tr -d '[:space:]')"], capture_output=True, text=True)
    with open("/tmp/output", "w") as f:
        f.write(result.stdout)

# Define the Generate Random Number component
@dsl.component(
    base_image="python:3.8",
    packages_to_install=["numpy"],
)
def generate_random_number(low: int, high: int):
    # Generate a random number within the specified range
    result = subprocess.run(["sh", "-c", f"echo $((RANDOM % ({high} - {low}) + {low}))"], capture_output=True, text=True)
    with open("/tmp/output", "w") as f:
        f.write(result.stdout)

# Define the Print component
@dsl.component(
    base_image="python:3.8",
    packages_to_install=["numpy"],
)
def print_msg(msg: str):
    # Print a message to the console
    print(msg)

# Define the Conditional Execution Logic component
@dsl.pipeline(name="Conditional execution pipeline")
def condition():
    # Flip the coin
    flip_result = flip_coin()
    
    # Conditionally generate and print a random number
    if flip_result.output == "heads":
        random_num_heads = generate_random_number(low=0, high=9)
        print_msg(msg=f"Random number generated: {random_num_heads.output}")
        
        # Conditionally print a message based on the random number
        if int(random_num_heads.output) > 5:
            print_msg(msg="Number is greater than 5")
        else:
            print_msg(msg="Number is less than or equal to 5")
    elif flip_result.output == "tails":
        random_num_tails = generate_random_number(low=10, high=19)
        print_msg(msg=f"Random number generated: {random_num_tails.output}")
        
        # Conditionally print a message based on the random number
        if int(random_num_tails.output) > 15:
            print_msg(msg="Number is greater than 15")
        else:
            print_msg(msg="Number is less than or equal to 15")

# Compile the pipeline to a YAML file
kfp.compiler.Compiler().compile(condition, "condition.yaml")
```

This code defines a Kubeflow Pipeline named `Conditional execution pipeline` that performs a series of conditional operations based on the outcome of a coin flip. The pipeline consists of four components: `flip_coin`, `generate_random_number`, `print_msg`, and `condition`. The `condition` component uses nested `dsl.Condition` statements to control the execution flow. The pipeline uses Python and the `kfp` library for Kubeflow Pipelines.