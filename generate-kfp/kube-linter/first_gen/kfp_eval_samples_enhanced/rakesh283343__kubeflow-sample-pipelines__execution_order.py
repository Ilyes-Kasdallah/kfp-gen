from kfp import pipeline, component


# Define the execution_order pipeline
@pipeline(name="Execution order pipeline")
def execution_order():
    # Define the echo1 component
    @component(name="echo1")
    def echo1(text1="message 1"):
        # Execute the echo command using a bash container
        return f"echo {text1}"

    # Define the echo2 component
    @component(name="echo2")
    def echo2(text2):
        # Execute the echo command using a bash container
        return f"echo {text2}"

    # Define the main function to run the pipeline
    @component(name="main")
    def main():
        # Call the echo1 component
        result1 = echo1()
        # Call the echo2 component
        result2 = echo2(result1)
        # Return the combined result
        return result2


# Run the pipeline
if __name__ == "__main__":
    execution_order().run()
