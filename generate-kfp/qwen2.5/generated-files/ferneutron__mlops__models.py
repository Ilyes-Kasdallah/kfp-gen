
from kfp import dsl

@dsl.pipeline(name="IrisClassificationPipeline")
def iris_classification_pipeline(train_dataset: dsl.Dataset):
    # Define the decision tree component
    @dsl.component(name="decision_tree")
    def decision_tree(input_data: dsl.InputDataset):
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score

        # Load the dataset
        data = input_data.read_csv()

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(data.drop("species", axis=1), data["species"], test_size=0.2, random_state=42)

        # Train the decision tree model
        model = DecisionTreeClassifier(random_state=42)
        model.fit(X_train, y_train)

        # Make predictions on the test set
        predictions = model.predict(X_test)

        # Calculate accuracy
        accuracy = accuracy_score(y_test, predictions)

        # Return the model and accuracy
        return model, accuracy

# Example usage
iris_classification_pipeline(train_dataset="path/to/iris.csv")
