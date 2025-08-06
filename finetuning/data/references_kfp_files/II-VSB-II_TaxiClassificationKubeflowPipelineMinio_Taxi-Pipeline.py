import kfp
from kfp import components
from kfp import dsl
from kfp import gcp
from kfp import onprem
from kubernetes.client.models import V1EnvVar


secretKey = V1EnvVar(name='MINIO_SECRET_KEY', value='minio123')
accessKey = V1EnvVar(name='MINIO_ACCESS_KEY', value='minio')
minio_endpoint = V1EnvVar(name='MINIO_ENDPOINT', value='minio-service:9000')

platform = 'local'

#proxy="http://test:8080"
proxy = ""

dataflow_tf_data_validation_op  = components.load_component_from_url(
  'https://raw.githubusercontent.com/II-VSB-II/TaxiClassificationKubeflowPipelineMinio/main/yamls/tfdv_component.yaml')
dataflow_tf_transform_op        = components.load_component_from_url(
  'https://raw.githubusercontent.com/II-VSB-II/TaxiClassificationKubeflowPipelineMinio/main/yamls/tft_component.yaml')
tf_train_op                     = components.load_component_from_url(
  'https://raw.githubusercontent.com/II-VSB-II/TaxiClassificationKubeflowPipelineMinio/main/yamls/dnntrainer_component.yaml')
dataflow_tf_model_analyze_op    = components.load_component_from_url(
  'https://raw.githubusercontent.com/II-VSB-II/TaxiClassificationKubeflowPipelineMinio/main/yamls/tfma_component.yaml')
dataflow_tf_predict_op          = components.load_component_from_url(
  'https://raw.githubusercontent.com/II-VSB-II/TaxiClassificationKubeflowPipelineMinio/main/yamls/predict_component.yaml')

confusion_matrix_op             = components.load_component_from_url(
  'https://raw.githubusercontent.com/II-VSB-II/TaxiClassificationKubeflowPipelineMinio/main/yamls/confusion_matrix_component.yaml')
roc_op                          = components.load_component_from_url(
  'https://raw.githubusercontent.com/II-VSB-II/TaxiClassificationKubeflowPipelineMinio/main/yamls/roc_component.yaml')

@dsl.pipeline(
  name='TFX Taxi Cab Classification Pipeline Example',
  description='Example pipeline that does classification with model analysis based on a public BigQuery dataset.'
)
def taxi_cab_classification(
    project,
    output="/mnt/shared",
    column_names='/mnt/shared/pipelines/column-names.json',
    key_columns='trip_start_timestamp',
    train='/mnt/shared/pipelines/train.csv',
    evaluation='/mnt/shared/pipelines/eval.csv',
    mode='local',
    preprocess_module='/mnt/shared/pipelines/preprocessing.py',
    learning_rate=0.1,
    hidden_layer_size='1500',
    steps=3000,
    analyze_slice_column='trip_start_hour'
):
    output_template = str(output) + '/{{workflow.uid}}/{{pod.name}}/data'
    target_lambda = """lambda x: (x['target'] > x['fare'] * 0.2)"""
    target_class_lambda = """lambda x: 1 if (x['target'] > x['fare'] * 0.2) else 0"""

    tf_server_name = 'taxi-cab-classification-model-{{workflow.uid}}'

    if platform != 'GCP':
        vop = dsl.VolumeOp(
            name="create_pvc",
            resource_name="pipeline-pvc",
            modes=dsl.VOLUME_MODE_RWM,
            size="1Gi"
        )
        if proxy != "":
            checkout = dsl.ContainerOp(
            name="checkout",
            image="alpine/git:latest",
            command=["git", "clone", "https://github.com/II-VSB-II/TaxiClassificationKubeflowPipelineMinio.git", str(output) + 
                     "/pipelines", "-c", "http.proxy={}".format(proxy)],
        ).apply(onprem.mount_pvc(vop.outputs["name"], 'local-storage', output))
        else:
            checkout = dsl.ContainerOp(
            name="checkout",
            image="alpine/git:latest",
            command=["git", "clone", "https://github.com/II-VSB-II/TaxiClassificationKubeflowPipelineMinio.git", str(output) + "/pipelines"],
        ).apply(onprem.mount_pvc(vop.outputs["name"], 'local-storage', output))
            
        
        checkout.after(vop)

    validation = dataflow_tf_data_validation_op(
        inference_data=train,
        validation_data=evaluation,
        column_names=column_names,
        key_columns=key_columns,
        gcp_project=project,
        run_mode=mode,
        validation_output=output_template,
    )
    if platform != 'GCP':
        validation.after(checkout)

    preprocess = dataflow_tf_transform_op(
        training_data_file_pattern=train,
        evaluation_data_file_pattern=evaluation,
        schema=validation.outputs['schema'],
        gcp_project=project,
        run_mode=mode,
        preprocessing_module=preprocess_module,
        transformed_data_dir=output_template
    )

    training = tf_train_op(
        transformed_data_dir=preprocess.output,
        schema=validation.outputs['schema'],
        learning_rate=learning_rate,
        hidden_layer_size=hidden_layer_size,
        steps=steps,
        target='tips',
        preprocessing_module=preprocess_module,
        training_output_dir=output_template
    )

    analysis = dataflow_tf_model_analyze_op(
        model=training.output,
        evaluation_data=evaluation,
        schema=validation.outputs['schema'],
        gcp_project=project,
        run_mode=mode,
        slice_columns=analyze_slice_column,
        analysis_results_dir=output_template
    ).add_env_variable(secretKey).add_env_variable(accessKey).add_env_variable(minio_endpoint)

    prediction = dataflow_tf_predict_op(
        data_file_pattern=evaluation,
        schema=validation.outputs['schema'],
        target_column='tips',
        model=training.output,
        run_mode=mode,
        gcp_project=project,
        predictions_dir=output_template
    ).add_env_variable(secretKey).add_env_variable(accessKey).add_env_variable(minio_endpoint)


    cm = confusion_matrix_op(
        predictions=prediction.output,
        target_lambda=target_lambda,
        output_dir=output_template
    ).add_env_variable(secretKey).add_env_variable(accessKey).add_env_variable(minio_endpoint)

    roc = roc_op(
        predictions_dir=prediction.output,
        target_lambda=target_class_lambda,
        output_dir=output_template
    ).add_env_variable(secretKey).add_env_variable(accessKey).add_env_variable(minio_endpoint)


    steps = [validation, preprocess, training, analysis, prediction, cm, roc]
    
    for step in steps:
        step.apply(onprem.mount_pvc(vop.outputs["name"], 'local-storage', output))


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(taxi_cab_classification, "TaxiPipelineMinio" + '.zip')
