```python
import kfp
from kfp import dsl
from kfp.components import load_component

# Load components from the Ark-kun/pipeline_components repository
load_component('https://raw.githubusercontent.com/Ark-kun/pipeline-components/master/components/data_loading/chicago_taxi_dataset.yaml')
load_component('https://raw.githubusercontent.com/Ark-kun/pipeline-components/master/components/data_preprocessing/pandas_transform_csv.yaml')
load_component('https://raw.githubusercontent.com/Ark-kun/pipeline-components/master/components/data_preprocessing/drop_header.yaml')
load_component('https://raw.githubusercontent.com/Ark-kun/pipeline-components/master/components/model_training/xgboost_train_on_csv.yaml')
load_component('https://raw.githubusercontent.com/Ark-kun/pipeline-components/master/components/model_prediction/xgboost_predict_on_csv.yaml')
load_component('https://raw.githubusercontent.com/Ark-kun/pipeline-components/master/components/metrics/calculate_regression_metrics_from_csv.yaml')

def train_until_good():
    # Load the Chicago Taxi Trips dataset
    chicago_taxi_dataset = chicago_taxi_dataset_op()
    
    # Preprocess the data
    transformed_data = pandas_transform_csv_op(chicago_taxi_dataset)
    cleaned_data = drop_header_op(transformed_data)
    
    # Train the model
    initial_model = None  # Placeholder for the initial model
    trained_model = xgboost_train_on_csv_op(cleaned_data, initial_model, 'fare_amount', 'reg:squarederror', 1000)
    
    # Predict on the same data
    predictions = xgboost_predict_on_csv_op(cleaned_data, trained_model)
    
    # Calculate regression metrics
    metrics = calculate_regression_metrics_from_csv_op(predictions, cleaned_data)
    
    # Check if the error is below a threshold
    if metrics['rmse'] < 0.1:
        return trained_model
    else:
        # Recursively call the function with the new model and data
        return train_until_good(trained_model, cleaned_data)

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(train_until_good, package_path='train_until_good.tar.gz')
```

This code defines the `train_until_good` pipeline using the Kubeflow Pipelines SDK. It includes all the required components and orchestrates their execution according to the described logic. The pipeline starts by loading the Chicago Taxi Trips dataset, preprocessing the data, training an XGBoost model, making predictions, calculating regression metrics, and checking if the error is below a threshold. If the error is too high, the process repeats, leading to a recursive call to the `train_until_good` function.