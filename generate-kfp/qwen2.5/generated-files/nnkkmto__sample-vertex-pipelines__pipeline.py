
from kfp import pipeline
from kfp.components import text_split

@pipeline(name="sample-pipeline")
def sample_pipeline():
    # Define the split_sentence component
    split_sentence = text_split()

    # Define the main task
    @component(name="process_text")
    def process_text(sentence):
        # Split the sentence into words
        words = split_sentence(sentence)
        return words

    # Example usage
    input_sentence = "Hello world! This is a test."
    result = process_text(input_sentence)
    print(result)
