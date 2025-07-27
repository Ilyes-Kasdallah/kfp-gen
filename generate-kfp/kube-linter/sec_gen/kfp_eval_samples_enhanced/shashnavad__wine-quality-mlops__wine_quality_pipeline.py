import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@pipeline(name="wine_quality_pipeline")
def wine_quality_pipeline(data_path):
    # Load the dataset
    dataset = Dataset.from_csv(data_path)

    # Split the dataset into features and labels
    X, y = dataset.read_csv().drop(columns=["quality"])

    # Scale the features using StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Save the preprocessed features, labels, and scaler object
    Output[Dataset](X_scaled, name="scaled_features"),
    Output[Model](y, name="labels"),
    Output[Metrics](name="metrics")


# Compile the pipeline
kfp.compiler.Compiler().compile(wine_quality_pipeline)
