```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load the components
addition_op = load_component_from_file('02_addition_op.yaml')
multiplication_op = load_component_from_file('02_multiplication_op.yaml')

# Define the pipeline
@dsl.pipeline(name='Submitted Pipeline')
def submitted_pipeline(a=1.0, b=7.0):
    # First component: addition
    add_result = addition_op(a=a, b=b)
    
    # Second component: multiplication
    multiply_result = multiplication_op(sum=add_result.sum, product=add_result.product)

# Execute the pipeline
if __name__ == '__main__':
    from kfp.compiler import.Compiler
    compiler = Compiler()
    pipeline_spec = compiler.compile(submitted_pipeline, package_path='03_outputs_pipeline.yaml')
```

This code snippet defines a Kubeflow Pipeline named `Submitted Pipeline` that performs two arithmetic operations. The pipeline consists of two components, each taking two float inputs and returning a NamedTuple containing the sum and product of these inputs. The second component calculates a sum and product from the results of the first component. The pipeline's control flow is sequential, with the second component depending on the first component's output. The pipeline uses the `kfp.dsl` library from the Kubeflow Pipelines SDK. The pipeline has default input arguments `a=1.0` and `b=7.0`, but can be overridden during execution. The code leverages Python's `collections.namedtuple` for structured output. The pipeline also uses environment variables `KUBEFLOW_ENDPOINT` and `BEARER_TOKEN` for connecting to a Kubeflow instance.