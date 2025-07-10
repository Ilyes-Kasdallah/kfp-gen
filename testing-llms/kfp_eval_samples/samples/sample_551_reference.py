from kfp.dsl import pipeline, get_pipeline_conf

from src.maikube.components import load_component

@pipeline(name="process NFStream pipeline")
def process_nfstream_pipeline(input_bucket:str, input_pcap:str, output_bucket:str, output_file:str):
    minio_download = load_component('minio_download')
    minio_upload = load_component('minio_upload')
    nfstream = load_component('nfs_feature_extractoion')

    download_op = minio_download(f'kubeflow/{input_pcap_bucket}/{input_pcap_file}')
    process_op = nfstream(download_op.output)
    minio_upload(process_op.output, f'kubeflow/{output_bucket}/{output_file}')
    get_pipeline_conf().set_image_pull_policy(policy="Never")