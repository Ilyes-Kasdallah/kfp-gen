import kfp
from kfp.dsl import pipeline, component


# Define the pipeline
@pipeline(name="Pipeline")
def Pipeline():
    # Define the first component
    @component
    def component1():
        print("Executing component 1")
        return "Result from component 1"

    # Define the second component
    @component
    def component2():
        print("Executing component 2")
        return "Result from component 2"

    # Define the third component
    @component
    def component3():
        print("Executing component 3")
        return "Result from component 3"

    # Define the fourth component
    @component
    def component4():
        print("Executing component 4")
        return "Result from component 4"

    # Execute the pipeline
    component1()
    component2()
    component3()
    component4()


# Run the pipeline
if __name__ == "__main__":
    Pipeline()
