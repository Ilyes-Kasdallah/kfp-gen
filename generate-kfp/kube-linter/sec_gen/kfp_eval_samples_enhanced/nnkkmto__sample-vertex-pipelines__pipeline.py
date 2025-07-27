import kfp
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define the pipeline function
@pipeline(name="sample-pipeline")
def sample_pipeline():
    # Define the split_sentence component
    @component(name="split_sentence")
    def split_sentence(sentence):
        # Split the sentence into words
        words = sentence.split()
        return words

    # Define the main task
    @component(name="main_task")
    def main_task(words):
        # Example task: Print the words
        print(words)


# Compile the pipeline
kfp.compiler.Compiler().compile(sample_pipeline)
