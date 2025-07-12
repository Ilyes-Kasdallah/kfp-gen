```python
import kfp
from kfp import dsl
from kfp.components import load_component_from_url

# Load components from the specified GitHub repository
load_component_from_url(
    url='https://raw.githubusercontent.com/kubeflow/pipelines/0.2.4/components/xgboost/component.yaml',
    package_path='./components'
)
load_component_from_url(
    url='https://raw.githubusercontent.com/kubeflow/pipelines/0.2.4/components/pandas/component.yaml',
    package_path='./components'
)

# Define the main pipeline
@dsl.pipeline(name="train_until_good_pipeline")
def train_until_good_pipeline():
    # Load the Chicago Taxi Trips dataset
    chicago_taxi_dataset = load_component_from_url(
        url='https://raw.githubusercontent.com/kubeflow/pipelines/0.2.4/components/chicago-taxi-dataset/component.yaml',
        package_path='./components'
    )()

    # Preprocess the dataset
    drop_header = load_component_from_url(
        url='https://raw.githubusercontent.com/kubeflow/pipelines/0.2.4/components/drop-header/component.yaml',
        package_path='./components'
    )(input=chicago_taxi_dataset)

    pandas_transform_csv = load_component_from_url(
        url='https://raw.githubusercontent.com/kubeflow/pipelines/0.2.4/components/pandas-transform-csv/component.yaml',
        package_path='./components'
    )(input=drop_header)

    # Split the dataset into training and true values
    split_data = load_component_from_url(
        url='https://raw.githubusercontent.com/kubeflow/pipelines/0.2.4/components/split-data/component.yaml',
        package_path='./components'
    )(input=pandas_transform_csv)

    # Define the recursive training sub-pipeline
    @dsl.component
    def train_until_low_error(starting_model=None, training_data=split_data['training'], true_values=split_data['true']):
        if starting_model is None:
            starting_model = None
        else:
            starting_model = starting_model

        xgboost_train = load_component_from_url(
            url='https://raw.githubusercontent.com/kubeflow/pipelines/0.2.4/components/xgboost/train-on-csv/component.yaml',
            package_path='./components'
        )(input=training_data, starting_model=starting_model, label_column='fare_amount', objective='reg:squarederror', num_iterations=100)

        xgboost_predict = load_component_from_url(
            url='https://raw.githubusercontent.com/kubeflow/pipelines/0.2.4/components/xgboost/predict-on-csv/component.yaml',
            package_path='./components'
        )(input=training_data, model=xgboost_train.outputs['model'], label_column='fare_amount')

        calculate_metrics = load_component_from_url(
            url='https://raw.githubusercontent.com/kubeflow/pipelines/0.2.4/components/calculate-regression-metrics-from-csv/component.yaml',
            package_path='./components'
        )(input=true_values, predicted_values=xgboost_predict.outputs['predictions'])

        mean_squared_error = calculate_metrics.outputs['mean_squared_error']

        condition = dsl.Condition(mean_squared_error > 0.01)
        return condition, xgboost_train, xgboost_predict, calculate_metrics

    # Start the recursive training
    condition, xgboost_train, xgboost_predict, calculate_metrics = train_until_low_error()

    # Continue the pipeline based on the condition
    if condition:
        train_until_low_error(xgboost_train.outputs['model'])
```

This code snippet defines a Kubeflow Pipeline named `train_until_good_pipeline` that iteratively trains an XGBoost model on the Chicago Taxi Trips dataset until the Mean Squared Error falls below 0.01. The pipeline includes components for loading the dataset, preprocessing, splitting, and training the model. The recursive training logic is implemented within the `train_until_low_error` component, which uses a `kfp.dsl.Condition` to control the flow of the pipeline.