
from kubeflow.pipelines import compose

@dsl.pipeline(name="Data_Processing_and_Hyperparameter_Tuning")
def Data_Processing_and_Hyperparameter_Tuning():
    # Define the first component: Data Preprocessing
    preprocess = compose(
        "@dsl.component",
        "data_preprocessing",
        inputs=[
            "@dsl.input",
            "@dsl.output"
        ],
        outputs=[
            "@dsl.output"
        ],
        operations=[
            "@dsl.operation",
            "load_data",
            "clean_data",
            "transform_data"
        ]
    )

    # Define the second component: Hyperparameter Tuning
    tune_hyperparameters = compose(
        "@dsl.component",
        "hyperparameter_tuning",
        inputs=[
            "@dsl.input",
            "@dsl.output"
        ],
        outputs=[
            "@dsl.output"
        ],
        operations=[
            "@dsl.operation",
            "train_model",
            "evaluate_model"
        ]
    )

    # Define the third component: Model Evaluation
    evaluate_model = compose(
        "@dsl.component",
        "model_evaluation",
        inputs=[
            "@dsl.input",
            "@dsl.output"
        ],
        outputs=[
            "@dsl.output"
        ],
        operations=[
            "@dsl.operation",
            "predict_results"
        ]
    )

    # Combine all components into a single pipeline
    return preprocess + tune_hyperparameters + evaluate_model
