
from kfp import dsl

@dsl.pipeline(name="head-pose-pipeline")
def head_pose_pipeline():
    # Define the training component
    training = dsl.component(
        name="training",
        description="Trains a head-pose estimation model",
        image="your-training-image",
        command=["python", "train_head_pose.py"],
        inputs=[
            dsl.input("input_data", type="string"),
            dsl.input("model_config", type="dict")
        ],
        outputs=[
            dsl.output("model", type="object")
        ]
    )

    # Define the evaluation component
    evaluation = dsl.component(
        name="evaluation",
        description="Evaluates the head-pose estimation model",
        image="your-evaluation-image",
        command=["python", "evaluate_head_pose.py"],
        inputs=[
            dsl.input("model", type="object"),
            dsl.input("test_data", type="string")
        ],
        outputs=[
            dsl.output("results", type="dict")
        ]
    )

    # Return the pipeline
    return training, evaluation
