```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_file

# Load the components
choose_best_model = load_component_from_file('choose_best_model.yaml')
load_test_data = load_component_from_file('load_test_data.yaml')

# Define the pipeline
@dsl.pipeline(name='model_evaluation')
def model_evaluation(test_dataset, decision_tree_model, random_forest_model):
    # Load the test data
    test_data = load_test_data(test_dataset)
    
    # Choose the best model
    choose_best_model(
        test_dataset=test_data,
        decision_tree_model=decision_tree_model,
        random_forest_model=random_forest_model
    )

# Compile the pipeline
kfp.compiler.Compiler().compile(model_evaluation, 'evaluation.py')
```

In this solution, we define a Kubeflow Pipeline named `model_evaluation` using the `@dsl.pipeline` decorator. We load the `choose_best_model` and `load_test_data` components from separate YAML files using `load_component_from_file`. Inside the pipeline, we use the `load_test_data` component to load the test dataset, and then call the `choose_best_model` component to compare and select the best model based on accuracy scores. Finally, we compile the pipeline using the `Compiler()` class from the `kfp.compiler` module.