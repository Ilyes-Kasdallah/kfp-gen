
from kfp import dsl

@dsl.pipeline(name="Execution order pipeline")
def execution_order():
    # Define the first component: echo1
    @dsl.component(name="echo1")
    def echo1(text1="message 1"):
        # Execute the echo command using a bash container
        return f"echo {text1}"

    # Define the second component: echo2
    @dsl.component(name="echo2")
    def echo2(text2):
        # Execute the echo command using a bash container
        return f"echo {text2}"

    # Define the pipeline function
    @dsl.function(name="execution_order")
    def execution_order():
        # Call the components in sequence
        result1 = echo1()
        result2 = echo2(result1)
        return result2

# Run the pipeline
execution_order()
