from kfp import dsl

@dsl.component(
    base_image="unittest-image",
    image_pull_policy="Never"
)
def pipeline(param1: float = 0.3, param2: int = 42, param3: str = "2022-02-24"):
    """Kedro pipeline"""
    import subprocess
    subprocess.run(["kedro", "run"])

@dsl.pipeline(name="OnePodKedroPipeline")
def pipeline():
    pipeline_op = pipeline()