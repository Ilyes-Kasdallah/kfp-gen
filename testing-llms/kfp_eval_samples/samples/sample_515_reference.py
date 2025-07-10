# kfp_pipeline/components/split_data.py
from kfp import dsl
from kfp.dsl import OutputPath
import pandas as pd
import s3fs
import os

@dsl.component(
    base_image="python:3.10",  # 推荐自定义镜像以加速
    packages_to_install=["pandas", "s3fs"]
)
def split_data(
    csv_uri: str,
    train_csv: OutputPath(str),
    stream_csv: OutputPath(str),
    ratio: float = 0.4
):
    """
    组件功能:
    • csv_uri: 必须是 s3://bucket/key.csv
    • 按 ratio 切分数据，输出 train_csv / stream_csv

    环境变量:
    - MINIO_KEY
    - MINIO_SECRET
    - MINIO_ENDPOINT
    """
    # 1️⃣ 连接 S3 (MinIO)
    fs = s3fs.S3FileSystem(
        key=os.getenv("MINIO_KEY", "minio"),
        secret=os.getenv("MINIO_SECRET", "minio123"),
        client_kwargs={
            "endpoint_url": os.getenv("MINIO_ENDPOINT", "http://minio.kubeflow:9000"),
            "region_name": "us-east-1"  # 通常保持默认，对 MinIO 无强制要求
        }
    )

    # 2️⃣ 读取数据
    with fs.open(csv_uri, "rb") as f:
        df = (
            pd.read_csv(f)
            .replace(['<not counted>', ' '], pd.NA)
            .dropna()
        )

    # 3️⃣ 切分 & 保存
    cut = int(len(df) * ratio)
    df.iloc[:cut].to_csv(train_csv, index=False)
    df.iloc[cut:].to_csv(stream_csv, index=False)

    print(f"[split] rows={len(df)}  ratio={ratio}")
    print("train_csv →", train_csv)
    print("stream_csv→", stream_csv)



