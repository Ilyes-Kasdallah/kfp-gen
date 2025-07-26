
from kfp import pipeline
from kfp.components import DownloadDataset

@dsl.pipeline(name="CBIS-DDSM-Training-Pipeline")
def cbis_ddsm_training_pipeline():
    # Download the CBIS-DDSM dataset
    download_dataset = DownloadDataset(
        name="download_dataset",
        image="davidnet/cbis_ddsm_dataloader:1.0.2"
    )
    
    # Output the downloaded dataset
    output_artifact = download_dataset.output

    return output_artifact
