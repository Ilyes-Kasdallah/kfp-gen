from kfp import dsl

@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas==2.2.2"]
)
def load_data(data_output: dsl.Output[dsl.Artifact]):
    import pandas as pd
    import numpy as np
    import urllib.request
    import os
    
    # Download and consolidate datasets
    url1 = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    url2 = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.names"
    
    def download(url):
        filename = os.path.basename(url)
        if not os.path.exists(filename):
            urllib.request.urlretrieve(url, filename)
    
    download(url1)
    download(url2)
    
    df1 = pd.read_csv("pima-indians-diabetes.data.csv")
    df2 = pd.read_csv("pima-indians-diabetes.names", header=None)
    
    df = pd.concat([df1, df2], axis=1)
    df.columns = ["pregnancies", "glucose", "blood_pressure", "skin_thickness", "insulin", "bmi", "diabetes_pedigree_function", "age", "class"]
    
    # Clean data
    df = df[df["class"] != "No Info"]
    df = df.dropna()
    df["gender"] = df["gender"].replace({"M": 0, "F": 1})
    df["insulin"] = df["insulin"].fillna(df["insulin"].mean())
    
    # Save preprocessed data
    df.to_csv(data_output.path, index=False)

@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas==2.2.2", "scikit-learn==1.5.1"]
)
def prepare_data(data_input: dsl.Input[dsl.Artifact],
                 X_train_output: dsl.Output[dsl.Artifact],
                 X_test_output: dsl.Output[dsl.Artifact],
                 Y_train_output: dsl.Output[dsl.Artifact],
                 Y_test_output: dsl.Output[dsl.Artifact],
                 X_val_output: dsl.Output[dsl.Artifact],
                 Y_val_output: dsl.Output[dsl.Artifact]):
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    
    # Load preprocessed data
    df = pd.read_csv(data_input.path)
    
    # Separate features and target
    X = df.drop("class", axis=1)
    Y = df["class"]
    
    # Split data
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.25, random_state=42)
    
    # Save splits
    X_train.to_csv(X_train_output.path, index=False)
    X_test.to_csv(X_test_output.path, index=False)
    Y_train.to_csv(Y_train_output.path, index=False)
    Y_test.to_csv(Y_test_output.path, index=False)
    X_val.to_csv(X_val_output.path, index=False)
    Y_val.to_csv(Y_val_output.path, index=False)

@dsl.component(
    base_image="python:3.9",
    packages_to_install=["pandas==2.2.2", "scikit-learn==1.5.1"]
)
def train_model(X_train: dsl.Input[dsl.Artifact],
                Y_train: dsl.Input[dsl.Artifact],
                X_val: dsl.Input[dsl.Artifact],
                Y_val: dsl.Input[dsl.Artifact],
                model_output: dsl.Output[dsl.Model],
                accuracy_output: dsl.Output[dsl.Artifact]):
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score
    
    # Load data
    X_train_df = pd.read_csv(X_train.path)
    Y_train_df = pd.read_csv(Y_train.path)
    X_val_df = pd.read_csv(X_val.path)
    Y_val_df = pd.read_csv(Y_val.path)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_df, Y_train_df)
    
    # Evaluate model
    Y_pred = model.predict(X_val_df)
    accuracy = accuracy_score(Y_val_df, Y_pred)
    
    # Save model
    import joblib
    joblib.dump(model, model_output.path)
    
    # Save accuracy
    with open(accuracy_output.path, "w") as f:
        f.write(str(accuracy))

@dsl.pipeline(name="DiabetesPredictionPipeline")
def diabetes_prediction_pipeline():
    load_data_task = load_data()
    prepare_data_task = prepare_data(data_input=load_data_task.outputs["data_output"])
    train_model_task = train_model(
        X_train=prepare_data_task.outputs["X_train_output"],
        Y_train=prepare_data_task.outputs["Y_train_output"],
        X_val=prepare_data_task.outputs["X_val_output"],
        Y_val=prepare_data_task.outputs["Y_val_output"],
        model_output=dsl.Output[dsl.Model](),
        accuracy_output=dsl.Output[dsl.Artifact]()
    )