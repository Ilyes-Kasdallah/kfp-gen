# kfp_pipeline/build_pipeline.py
import pathlib, sys, kfp
from kfp import dsl

# ────────── 常量 & 路径 ─────────────────────────────────── #
ROOT  = pathlib.Path(__file__).resolve().parents[1]
COMP  = ROOT / "kfp_pipeline" / "components"
IMAGE = "hirschazer/flux_demo5:latest"      # 你的业务镜像

# 让 Python 找得到 components 包
sys.path.append(str(COMP.parent))

# ────────── 导入已装饰好的组件函数 ─────────────────────── #
from components.split_data          import split_data
from components.offline_train       import offline_train
from components.launch_katib        import launch_katib
from components.apply_k8s_resource  import apply_k8s_resource

# 如需统一镜像，可在这里动态覆写（任选）
for c in (split_data, offline_train, launch_katib):
    c.component_spec.implementation.container.image = IMAGE

# ────────── DAG 定义 ──────────────────────────────────── #
@dsl.pipeline(
    name="twin-stream-pipeline",
    description="Katib HPO → Batch 训练 → Streaming Job"
)
def pipeline(
    csv_uri: str = "s3://katib-flux-demo/datasets/load_stimulus_global.csv",
):
    # ① 40/60 切分，自动把 train/stream.csv 上传回同 Bucket
    split = split_data(csv_uri=csv_uri)

    # ② Katib 随机搜索
    hpo = launch_katib(
        train_image = IMAGE,
        train_csv   = split.outputs["train_csv"],
        out_dir     = "/mnt/data",
    )

    # ③ 离线 Batch 训练
    train = offline_train(
        csv       = split.outputs["train_csv"],
        model_key = "models/ann_batch_model.pth",
    ).after(hpo)

    # ④ kubectl apply Producer + Consumer Job
    apply_k8s_resource(
        yaml_path = str(COMP / "stream_job.yaml"),
    ).after(train)

# ────────── 编译 + 可选：自动触发一次 Run ─────────────── #
if __name__ == "__main__":
    pkg = str(ROOT / "pipeline.json")
    kfp.compiler.Compiler().compile(
        pipeline_func = pipeline,
        package_path  = pkg,
    )
    print("✅  pipeline.json generated")

    # ----- 自动触发（可删掉） -----
    from kfp import Client
    client = Client(host="http://ml-pipeline.kubeflow:8888")  # in-cluster 可省 host
    run = client.create_run_from_pipeline_package(
        pipeline_file   = pkg,
        arguments       = {"csv_uri": "s3://katib-flux-demo/datasets/load_stimulus_global.csv"},
        experiment_name = "twin-stream",
        run_name        = "twin-stream-auto",
    )
    print("🚀  triggered run:", run.run_id)


