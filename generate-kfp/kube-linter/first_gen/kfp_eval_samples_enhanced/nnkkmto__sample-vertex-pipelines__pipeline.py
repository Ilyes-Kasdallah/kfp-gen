import kfp
from kfp.dsl import pipeline, component


@dsl.pipeline(name="sample-pipeline")
def sample_pipeline():
    # Define the split_sentence component
    @component
    def split_sentence(sentence):
        # Split the sentence into words using basic string splitting
        words = sentence.split()
        return words

    # Define the main component that uses the split_sentence component
    @component
    def main_component(words):
        # Process the list of words
        processed_words = [word.upper() for word in words]
        return processed_words


# Execute the pipeline
if __name__ == "__main__":
    sample_pipeline()
