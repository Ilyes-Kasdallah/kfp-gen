```python
from kfp import dsl
from kfp.components import load_component_from_text

# Load the component from text
_save_message_to_file = load_component_from_text("""
name: save-message-to-file
description: Saves a message to a GCS file
inputs:
- {type: STRING, description: Message to be written}
- {type: STRING, description: GCS path where the message should be saved}
outputs:
- {}
implementation:
  container:
    image: python:3.10
    command:
      - /bin/bash
      - -c
      - |
        echo "$1" > "$2"
""")

# Define the pipeline
@dsl.pipeline(name="sample-pipeline")
def sample_pipeline(message: str, gcs_filepath: str):
    # Call the component
    _save_message_to_file(message=message, gcs_filepath=gcs_filepath)
```

In this solution, we first load the component from text using `load_component_from_text`. We then define the pipeline using the `@dsl.pipeline` decorator with the name "sample-pipeline". Inside the pipeline, we call the `_save_message_to_file` component with the provided `message` and `gcs_filepath` inputs. This completes the definition of the Kubeflow Pipeline named `sample-pipeline`.