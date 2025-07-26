import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

# Define the pipeline function name
kfp_pipeline_xgboost = "diabetes_prediction_pipeline"


# Define the load_data component
@component
def load_data(url1, url2):
    """
    Load data from two CSV files located at specified URLs.

    Args:
    url1 (str): URL of the first CSV file.
    url2 (str): URL of the second CSV file.

    Returns:
    pd.DataFrame: Loaded data.
    """
    # Load data from CSV files
    df1 = pd.read_csv(url1)
    df2 = pd.read_csv(url2)

    # Handle missing values and perform data cleaning
    df1.fillna(df1.mean(), inplace=True)
    df2.fillna(df2.mean(), inplace=True)

    # Rename columns based on a mapping
    df1.columns = ["age", "sex", "bmi", "chol", "glucose", "insulin", "target"]
    df2.columns = ["age", "sex", "bmi", "chol", "glucose", "insulin", "target"]

    # Convert categorical data to numerical representations
    df1["sex"] = df1["sex"].map({"male": 0, "female": 1})
    df2["sex"] = df2["sex"].map({"male": 0, "female": 1})

    return df1, df2


# Define the diabetes_prediction component
@component
def diabetes_prediction(data1, data2):
    """
    Predict diabetes using XGBoost.

    Args:
    data1 (pd.DataFrame): Data from the first CSV file.
    data2 (pd.DataFrame): Data from the second CSV file.

    Returns:
    float: Accuracy score of the model.
    """
    # Split data into features and target
    X1, y1 = data1.drop("target", axis=1), data1["target"]
    X2, y2 = data2.drop("target", axis=1), data2["target"]

    # Combine data into a single DataFrame
    combined_data = pd.concat([X1, X2], axis=1)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        combined_data, y1, test_size=0.2, random_state=42
    )

    # Initialize and train the XGBoost model
    model = Pipeline([("scaler", StandardScaler()), ("model", xgb.XGBClassifier())])

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)

    return accuracy


# Define the pipeline
@pipeline(name=kfp_pipeline_xgboost)
def diabetes_prediction_pipeline():
    """
    Pipeline to predict diabetes using XGBoost.
    """
    data1, data2 = load_data("data1.csv", "data2.csv")
    accuracy = diabetes_prediction(data1, data2)
    print(f"Accuracy: {accuracy}")


# Run the pipeline
diabetes_prediction_pipeline()
