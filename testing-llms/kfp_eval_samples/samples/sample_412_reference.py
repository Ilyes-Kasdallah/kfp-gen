# pipeline.py
from kfp import dsl, compiler
from components.data_acquisition import acquire_dataset
from components.feature_preparation import prepare_features
from components.model_development import develop_model
from components.performance_assessment import assess_performance

@dsl.pipeline(name="iris-classification-pipeline")
def classification_pipeline():
    """Orchestrate the end-to-end classification pipeline."""
    # Data acquisition
    data_op = acquire_dataset()
    
    # Feature preparation
    prep_op = prepare_features(raw_dataset=data_op.outputs["dataset_output"])
    
    # Model development
    model_op = develop_model(
        training_features=prep_op.outputs["training_features"],
        training_labels=prep_op.outputs["training_labels"]
    )
    
    # Performance assessment - Fixed the output reference
    assess_op = assess_performance(
        testing_features=prep_op.outputs["testing_features"],
        testing_labels=prep_op.outputs["testing_labels"],  # This was the issue
        trained_model=model_op.outputs["model_artifact"]
    )

if __name__ == "__main__":
    compiler.Compiler().compile(
        pipeline_func=classification_pipeline,
        package_path="iris_pipeline.yaml"
    )