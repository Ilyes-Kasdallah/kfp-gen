from kfp import pipeline
from kfp.dsl import component


@dsl.pipeline(name="collected_parameters_pipeline")
def collected_parameters():
    # Define the split_ids component
    @component
    def split_ids(model_ids: str) -> list:
        # Split the input string by commas and return the list
        return model_ids.split(",")

    # Define the main function that uses the split_ids component
    @component
    def main(model_ids: str) -> list:
        # Call the split_ids function and print the result
        result = split_ids(model_ids)
        print(result)


# Example usage
if __name__ == "__main__":
    # Example usage of the main function
    main("s1,s2,s3")
