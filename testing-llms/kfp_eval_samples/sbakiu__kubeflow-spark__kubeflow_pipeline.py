```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load components
spark_job_submission = load_component_from_file('k8s-apply-component.yaml')
spark_app_status_checker = load_component_from_file('k8s-get-component.yaml')
print_completion_message = load_component_from_file('print-completion-message.yaml')

# Define the pipeline
@dsl.pipeline(name='Spark Operator job pipeline')
def spark_operator_job_pipeline(spark_job_definition_path):
    # Submit Spark job
    spark_job_name = dsl.OutputPath('spark_job_name')
    spark_job_submission(spark_job_definition_path=spark_job_definition_path,
                          output=spark_job_name)

    # Check Spark application status
    spark_app_state = dsl.OutputPath('spark_app_state')
    spark_app_status_checker(input=spark_job_name,
                             output=spark_app_state)

    # Wait for Spark application to complete
    while spark_app_state.value != 'COMPLETED':
        spark_app_status_checker(input=spark_job_name,
                                 output=spark_app_state)

    # Print completion message
    print_completion_message(input=spark_job_name)
```

This code snippet defines a Kubeflow Pipeline named `Spark Operator job pipeline` that performs a Spark job submission and monitors its status. The pipeline consists of three main components: Spark Job Submission, Spark Application Status Checker, and Print Completion Message. The pipeline utilizes the Kubeflow Pipelines DSL, Kubernetes `apply` and `get` components, and the `json` and `yaml` libraries for handling configuration data.