import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# Define the pipeline
@dsl.pipeline(name="metrics_visualization_pipeline")
def metrics_visualization_v2_test():
    # Load the wine dataset
    wine = load_wine()

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        wine.data, wine.target, test_size=0.2, random_state=42
    )

    # Standardize the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Create a pipeline with the wine classification component
    wine_classification = component(
        name="wine_classification",
        inputs={"X": X_train_scaled, "y": y_train},
        outputs={
            "metrics": {"classification_report": classification_report(y_test, y_pred)}
        },
    )

    # Run the pipeline
    wine_classification.run()


# Example usage
if __name__ == "__main__":
    metrics_visualization_v2_test()
