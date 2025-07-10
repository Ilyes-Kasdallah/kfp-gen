from kfp import dsl

@dsl.pipeline(
    name='Hello World',
    description='A pipeline to demonstrate use of PersistentVolumeClaim'
)
def pvc_pipeline(log:str ="/mnt/data/kubeflow",
                 data_folder_directory:str = "",
                 output_folder_directory:str="",
                 tmp_folder_directory:str="",
                 sampling_rate:float=0.001):
    #git clone
    def clone_equasim():
        return dsl.ContainerOp(
        name = 'Git Clone Equasim',
        image = 'zeynep02/pipeline-v0.0.4:latest',
        command = 'python3',
        arguments = [
            "/mnt/data/kubeflow/code/clone.py",  
            "--log_dir",
            log
           

        ],
        pvolumes={'/mnt/data/kubeflow': dsl.PipelineVolume(pvc='my-pvc')}
    )
    def edit_config():
        return dsl.ContainerOp(
        name = 'Edit Config Yml',
        image = 'zeynep02/pipeline-v0.0.4:latest',
        command = 'python3',
        arguments = [
            "/mnt/data/kubeflow/code/edit_config.py",
            "--log_dir",
            log,
            "--data_folder_directory",
            data_folder_directory,
            "--output_folder_directory",
            output_folder_directory,
            "--tmp_folder_directory",
            tmp_folder_directory,
            "--sampling_rate",
            sampling_rate

        ],
        pvolumes={'/mnt/data/kubeflow': dsl.PipelineVolume(pvc='my-pvc')}

        )
    
    def synpp():
        return dsl.ContainerOp(
        name='Run synp',
        image='zeynep02/pipeline-v0.0.4:latest',
        command='python3',
        arguments=[ 
            "/mnt/data/kubeflow/code/synpp.py",
            "--log_dir",
            log,],
        pvolumes={'/mnt/data/kubeflow': dsl.PipelineVolume(pvc='my-pvc')}
        )
    
    clone_git = clone_equasim()
    clone_git.execution_options.caching_strategy.max_cache_staleness = "P0D"

    update_config = edit_config()
    update_config.execution_options.caching_strategy.max_cache_staleness = "P0D"   
    update_config.after(clone_git)
    synpp_run = synpp()
    synpp_run.execution_options.caching_strategy.max_cache_staleness = "P0D" 
    synpp_run.after(update_config)



    

if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(pvc_pipeline, 'pipeline_v_4.yaml')
