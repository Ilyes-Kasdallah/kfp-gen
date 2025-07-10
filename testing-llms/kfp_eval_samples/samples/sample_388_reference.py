from kfp import dsl

@dsl.pipeline(
    name='My Kubeflow Pipeline',
    description='A pipeline that orchestrates an R script and a Python script.'
)
def my_pipeline():
    # Define the R script component
    r_script_op = dsl.ContainerOp(
        name='run-r-script',
        image='your-r-image:latest',  # Replace with your R Docker image
        command=['Rscript', '/scripts/script.R'],
        file_outputs={
            'output': '/output/output.txt'  # Adjust as necessary
        }
    )
    
    # Define the Python script component
    python_script_op = dsl.ContainerOp(
        name='run-python-script',
        image='your-python-image:latest',  # Replace with your Python Docker image
        command=['python', '/scripts/script.py'],
        arguments=['--input', r_script_op.outputs['output']],
        file_outputs={
            'output': '/output/output.txt'  # Adjust as necessary
        }
    )

    # Set dependencies
    python_script_op.after(r_script_op)

if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(my_pipeline, 'pipeline.yaml')