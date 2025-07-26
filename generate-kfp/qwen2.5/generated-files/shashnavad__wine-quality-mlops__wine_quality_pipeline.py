
from kfp import dsl

@dsl.pipeline(name="wine_quality_pipeline")
def wine_quality_pipeline(data_path):
    # Load the data
    data = dsl.read_csv(data_path)
    
    # Split the data into features and labels
    X = data.drop(columns=['quality'])
    y = data['quality']
    
    # Scale the features
    scaler = dsl.component(
        name="scale_features",
        inputs={
            "X": X,
        },
        outputs={
            "scaled_X": dsl.output("scaled_X"),
        },
        steps=[
            dsl.standard_scaler(input="X", output="scaled_X"),
        ],
    )
    
    # Save the preprocessed features, labels, and scaler object
    scaled_X.save("scaled_X.csv")
    y.save("y.csv")
    scaler.save("scaler.pkl")
