import os
from kfp import dsl

@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas", "kfp", "kubernetes", "requests", "pyyaml", "scikit-learn", "matplotlib", "seaborn", "numpy", "sklearn", "pandas", "plotly", "scipy", "scikit-learn", "kfp", "kubernetes", "requests", "pyyaml", "scikit-learn", "matplotlib", "seaborn", "numpy", "sklearn", "pandas", "plotly", "scipy"],
    output_component_file="./component.yaml"
)
def getDataEndpoints(train_dataset_id: str, test_dataset_id: str, namespace: str, run_name: str, result_name: str) -> (str, str, str, str):
    import requests
    import yaml
    import os
    import json
    from urllib.parse import quote_plus
    from kfp.v2.dsl import OutputPath

    # Load the YAML configuration
    with open('../../config.yaml') as f:
        config = yaml.safe_load(f)

    # Define the URL for the data endpoint retrieval service
    url = config['data-endpoint-service-url']

    # Define the query parameters
    params = {
        'train_dataset_id': train_dataset_id,
        'test_dataset_id': test_dataset_id,
        'namespace': namespace,
        'run_name': run_name,
        'result_name': result_name
    }

    # Make the GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the data endpoint URLs
        train_endpoint = data['train_endpoint']
        test_endpoint = data['test_endpoint']
        result_endpoint = data['result_endpoint']
        result_catalogid = data['result_catalogid']

        return train_endpoint, test_endpoint, result_endpoint, result_catalogid
    else:
        raise Exception(f"Failed to retrieve data endpoints. Status code: {response.status_code}")

@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas", "kfp", "kubernetes", "requests", "pyyaml", "scikit-learn", "matplotlib", "seaborn", "numpy", "sklearn", "pandas", "plotly", "scipy", "scikit-learn", "kfp", "kubernetes", "requests", "pyyaml", "scikit-learn", "matplotlib", "seaborn", "numpy", "sklearn", "pandas", "plotly", "scipy"],
    output_component_file="./visualize_table/component.yaml"
)
def visualizeTable(train_endpoint: str, train_dataset_id: str, namespace: str) -> None:
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import os
    from kfp.v2.dsl import OutputPath

    # Load the training dataset
    df_train = pd.read_csv(train_endpoint)

    # Visualize the distribution of the target variable
    plt.figure(figsize=(10, 6))
    sns.histplot(df_train['price'], bins=30, kde=True)
    plt.title('Distribution of House Prices')
    plt.xlabel('Price')
    plt.ylabel('Frequency')

    # Save the visualization to a file
    output_path = os.path.join('/tmp', f'{train_dataset_id}_price_distribution.png')
    plt.savefig(output_path)

    # Log the visualization path
    print(f'Visualization saved to: {output_path}')

    # Return the output path
    return output_path

@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas", "kfp", "kubernetes", "requests", "pyyaml", "scikit-learn", "matplotlib", "seaborn", "numpy", "sklearn", "pandas", "plotly", "scipy", "scikit-learn", "kfp", "kubernetes", "requests", "pyyaml", "scikit-learn", "matplotlib", "seaborn", "numpy", "sklearn", "pandas", "plotly", "scipy"],
    output_component_file="./train_model/component.yaml"
)
def trainModel(train_endpoint_path: str, test_endpoint_path: str, result_name: str, result_endpoint_path: str, train_dataset_id: str, test_dataset_id: str, namespace: str) -> None:
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error
    import os
    from kfp.v2.dsl import OutputPath

    # Load the training and test datasets
    df_train = pd.read_csv(train_endpoint_path)
    df_test = pd.read_csv(test_endpoint_path)

    # Separate features and target variable
    X_train = df_train.drop(columns=['price'])
    y_train = df_train['price']
    X_test = df_test.drop(columns=['price'])
    y_test = df_test['price']

    # Split the training data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

    # Initialize and train the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate the model on the validation set
    y_pred = model.predict(X_val)
    mse = mean_squared_error(y