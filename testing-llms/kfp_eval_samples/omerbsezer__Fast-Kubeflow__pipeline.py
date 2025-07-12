```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load pre-built components from YAML files
download_op = load_component_from_file('download.yaml')
decision_tree_op = load_component_from_file('decision_tree.yaml')
logistic_regression_op = load_component_from_file('logistic_regression.yaml')
svm_op = load_component_from_file('svm.yaml')
naive_bayes_op = load_component_from_file('naive_bayes.yaml')
xg_boost_op = load_component_from_file('xg_boost.yaml')

@dsl.pipeline(name='ML Models Pipeline')
def ml_models_pipeline():
    # Download the input data
    download_task = download_op()

    # Run the five machine learning model components in parallel
    decision_tree_task = decision_tree_op(download_task.output)
    logistic_regression_task = logistic_regression_op(download_task.output)
    svm_task = svm_op(download_task.output)
    naive_bayes_task = naive_bayes_op(download_task.output)
    xg_boost_task = xg_boost_op(download_task.output)

    # Show the results
    show_results_task = dsl.ContainerOp(
        name='Show Results',
        image='python:3.8-slim',
        command=['python', '-c', 'print("Decision Tree Accuracy:", decision_tree_task.outputs.accuracy)',
                'print("Logistic Regression Accuracy:", logistic_regression_task.outputs.accuracy)',
                'print("Support Vector Machine Accuracy:", svm_task.outputs.accuracy)',
                'print("Naive Bayes Accuracy:", naive_bayes_task.outputs.accuracy)',
                'print("XG Boost Accuracy:", xg_boost_task.outputs.accuracy)'],
        arguments=[],
        outputs=dsl.Outputs()
    )
```

This code snippet defines a Kubeflow Pipeline named `ML Models Pipeline` that downloads the input data, runs five machine learning model components in parallel, and then shows the accuracy scores of each model. The pipeline uses pre-built components loaded from YAML files, leveraging scikit-learn-like libraries for the machine learning algorithms.