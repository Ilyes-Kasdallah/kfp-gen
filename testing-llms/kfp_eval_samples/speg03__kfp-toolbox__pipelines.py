```python
import kfp
from kfp import dsl

# Define the pipeline
@dsl.pipeline(name='timestamp-pipeline')
def timestamp_pipeline(
    format='%Y%m%d%H%M%S',
    prefix='',
    suffix='',
    separator='-',
    tz_offset=0,
):
    # Define the component
    @dsl.component(
        base_image='python:3.8-slim',
        packages_to_install=['pytz'],
        output_artifact=dsl.OutputArtifact(type=dsl.ArtifactType.TEXT),
    )
    def generate_timestamp(format, prefix, suffix, separator, tz_offset):
        import datetime
        from pytz import timezone
        
        # Create a datetime object with the specified timezone offset
        dt = datetime.datetime.now(timezone('UTC') + datetime.timedelta(hours=tz_offset))
        
        # Format the timestamp
        timestamp = dt.strftime(format)
        
        # Add prefix, suffix, and separator
        result = f"{prefix}{timestamp}{separator}{suffix}"
        
        return result
    
    # Execute the component
    generate_timestamp_op = generate_timestamp(
        format=format,
        prefix=prefix,
        suffix=suffix,
        separator=separator,
        tz_offset=tz_offset,
    )

# Compile the pipeline
compiler.Compiler().compile(timestamp_pipeline, 'pipelines.yaml')

# Submit the pipeline run
client = kfp.Client()
run = client.create_run_from_pipeline_package(
    package_path='pipelines.yaml',
    arguments={
        'format': '%Y%m%d%H%M%S',
        'prefix': '',
        'suffix': '',
        'separator': '-',
        'tz_offset': 0,
    },
)
print(f"Run ID: {run.id}")
```

This code snippet defines a Kubeflow Pipeline named `timestamp-pipeline` that includes a single component `generate_timestamp`. The component takes several input parameters such as format, prefix, suffix, separator, and timezone offset, and returns a formatted timestamp string. The pipeline is compiled into a YAML file named `pipelines.yaml` and submitted to the Kubeflow Pipelines server to execute.