import kfp
from kfp.dsl import pipeline, component

# Import necessary modules
from pharmbio.pipelines_kensert_preprocess.test import preprocess


@dsl.pipeline(name="Kensert_CNN_test")
def Kensert_CNN_test(
    model_type: str = "Inception_v3",
    checkpoint_preprocess: bool = True,
    workspace_name: str = "kfp-workspace",
):
    # Define the preprocessing step
    preprocess_step = preprocess(
        model_type=model_type,
        checkpoint_preprocess=checkpoint_preprocess,
        workspace_name=workspace_name,
    )

    # Define the main component that will run the preprocessing step
    main_component = component(
        name="main_component",
        steps=[preprocess_step],
    )

    # Return the main component
    return main_component
