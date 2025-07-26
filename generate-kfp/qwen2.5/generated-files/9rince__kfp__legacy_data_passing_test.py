
from kfp import pipeline
from kfp.components import legacy_data_passing_test

@pipeline(name="data_passing_pipeline")
def data_passing_pipeline():
    # Define the main component
    @legacy_data_passing_test()
    def main():
        # Simulate data passing logic
        print("Data is being passed from source to destination.")
        return "Data passed successfully."

# Run the pipeline
if __name__ == "__main__":
    data_passing_pipeline()
