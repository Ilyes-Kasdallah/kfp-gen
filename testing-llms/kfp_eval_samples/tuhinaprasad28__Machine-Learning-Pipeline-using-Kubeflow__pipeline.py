```python
from kfp import dsl
from kfp.components import load_component

# Load the components from the YAML files
download_op = load_component('download_data/download_data.yaml')
decision_tree_op = load_component('decision_tree/decision_tree.yaml')
logistic_regression_op = load_component('logistic_regression/logistic_regression.yaml')
show_results_op = load_component('show_results/show_results.yaml')

# Define the pipeline
@dsl.pipeline(name='First Pipeline')
def first_pipeline():
    # Download the dataset
    download_task = download_op()

    # Train Decision Tree model
    decision_tree_task = decision_tree_op(download_task.output)

    # Train Logistic Regression model
    logistic_regression_task = logistic_regression_op(download_task.output)

    # Show results
    show_results_task = show_results_op(decision_tree_task.output, logistic_regression_task.output)
```

This code snippet defines a Kubeflow Pipeline named `First Pipeline` that performs a classification task using Decision Tree and Logistic Regression models. The pipeline consists of four components: `download`, `decision_tree`, `logistic_regression`, and `show_results`. The `download` component downloads the necessary data, which is then consumed by both the `decision_tree` and `logistic_regression` components. The accuracy scores from both models are printed to the console by the `show_results` component.