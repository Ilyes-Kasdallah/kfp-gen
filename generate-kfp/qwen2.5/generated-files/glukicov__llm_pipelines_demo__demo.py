
from kfp import dsl

@dsl.pipeline(name="demo_pipeline")
def demo():
    # Step 1: Get data from the data_source
    get_data = dsl.component(
        name="get_data",
        image=dsl.image_from_name("base_image"),
        command=["python", "-c", "import sys; print(sys.argv[1])"],
        parameters={
            "data_source": dsl.input_parameter("data_source")
        }
    )

    # Step 2: Process the data
    process_data = dsl.component(
        name="process_data",
        image=dsl.image_from_name("base_image"),
        command=["python", "-c", "print('Processing data')"]
    )

    # Step 3: Combine the results
    combine_results = dsl.component(
        name="combine_results",
        image=dsl.image_from_name("base_image"),
        command=["python", "-c", "print('Combining results')"]
    )

    # Combine the outputs of the three steps
    result = get_data(data_source) + process_data(data_source) + combine_results(data_source)

    return result
