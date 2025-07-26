
from kfp import dsl

@dsl.pipeline(name="DataSplitPipeline")
def DataSplitPipeline():
    # Load the raw data from a remote YAML file
    getRawData = dsl.component(
        "getRawData",
        source="https://raw.githubusercontent.com/pavan-kumar-99/ml-ops/master/components/getRawData.yaml"
    )

    # Split the dataset into training and testing sets
    testTrainSplit = dsl.component(
        "TestTrainSplit",
        inputs=[getRawData],
        outputs=["train_data.csv", "test_data.csv"]
    )

    return testTrainSplit
