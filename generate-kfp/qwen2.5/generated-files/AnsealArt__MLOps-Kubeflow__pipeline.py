
from kfp import pipeline
from kfp.components import DownloadAndPreprocessData

@pipeline(name="California Housing Prediction Pipeline")
def california_housing_prediction_pipeline(
    output_path: str,
    run_date: str,
    test_size: float = 0.2,
):
    # Download and preprocess the California housing dataset
    download_and_preprocess_data(
        output_path=output_path,
        run_date=run_date,
        test_size=test_size,
    )
