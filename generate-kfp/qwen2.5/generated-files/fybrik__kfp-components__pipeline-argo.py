
from kfp import pipeline
from kfp.components import get_data_endpoints

@dsl.pipeline(name="Fybrik housing price estimate pipeline")
def fybrik_housing_price_estimate_pipeline(
    train_dataset_id: str,
    test_dataset_id: str,
    namespace: str,
    run_name: str,
):
    # Define the data endpoints
    data_endpoints = get_data_endpoints(namespace=namespace, run_name=run_name)

    # Define the pipeline steps
    step1 = data_endpoints.get_data_from_dataset(
        train_dataset_id=train_dataset_id,
        namespace=namespace,
        run_name=run_name,
    )
    step2 = data_endpoints.get_data_from_dataset(
        test_dataset_id=test_dataset_id,
        namespace=namespace,
        run_name=run_name,
    )

    # Define the final step for price estimation
    final_step = step1 + step2

    return final_step
