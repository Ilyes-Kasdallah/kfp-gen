
from kfp import pipeline
from kfp.components import read_metadata

@pipeline(name="Time-Series-Forecast-Chicago-Taxi")
def time_series_forecast_chicago_taxi():
    # Read metadata from BigQuery
    metadata = read_metadata()

    # Define the pipeline components
    # Example component: Load data from BigQuery
    load_data = pipeline.component(
        name="load_data",
        inputs={
            "metadata": metadata,
        },
        outputs={
            "data": {
                "type": "pandas.DataFrame",
            },
        },
        steps=[
            pipeline.task(
                name="load_data_step",
                inputs={
                    "data": metadata["data"],
                },
                outputs={
                    "data": {
                        "type": "pandas.DataFrame",
                    },
                },
            ),
        ],
    )

    # Example component: Normalize data
    normalize_data = pipeline.component(
        name="normalize_data",
        inputs={
            "data": metadata["data"],
        },
        outputs={
            "data": {
                "type": "pandas.DataFrame",
            },
        },
        steps=[
            pipeline.task(
                name="normalize_data_step",
                inputs={
                    "data": metadata["data"],
                },
                outputs={
                    "data": {
                        "type": "pandas.DataFrame",
                    },
                },
            ),
        ],
    )

    # Example component: Forecast data
    forecast_data = pipeline.component(
        name="forecast_data",
        inputs={
            "data": metadata["data"],
        },
        outputs={
            "data": {
                "type": "pandas.DataFrame",
            },
        },
        steps=[
            pipeline.task(
                name="forecast_data_step",
                inputs={
                    "data": metadata["data"],
                },
                outputs={
                    "data": {
                        "type": "pandas.DataFrame",
                    },
                },
            ),
        ],
    )

    return load_data, normalize_data, forecast_data
