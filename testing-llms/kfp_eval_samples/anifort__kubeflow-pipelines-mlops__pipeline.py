```python
from kfp import dsl
from kfp.components import load_component_from_file

# Load the tfidf-vectoriser component
tfidf_vectoriser = load_component_from_file("path/to/tfidf-vectoriser.component.yaml")

# Define the pipeline
@dsl.pipeline(name="A Simple CI pipeline")
def vectorizing(data_path: str, vectorizer_gcs_location: str):
    # Execute the tfidf-vectoriser component
    tfidf_vectoriser_op = tfidf_vectoriser(
        data_path=data_path,
        vectorizer_gcs_location=vectorizer_gcs_location
    )
```

In this solution, we first load the `tfidf-vectoriser` component using `load_component_from_file`. We then define the `vectorizing` pipeline using the `@dsl.pipeline` decorator. Inside the pipeline, we execute the `tfidf-vectoriser` component using the `tfidf_vectoriser_op` variable. The `data_path` and `vectorizer_gcs_location` parameters are passed to the `tfidf_vectoriser` component as inputs.