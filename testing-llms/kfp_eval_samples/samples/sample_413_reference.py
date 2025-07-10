from kfp import dsl
from kfp.dsl import Output, Dataset, component

@dsl.component(base_image="python:3.9")
def acquire_dataset(dataset_output: Output[Dataset]):
    """Acquire and prepare the initial dataset."""
    import subprocess
    subprocess.run(["pip", "install", "pandas", "scikit-learn"], check=True)
    
    from sklearn.datasets import load_iris
    import pandas as pd
    
    raw_data = load_iris()
    dataset = pd.DataFrame(
        raw_data.data,
        columns=[name.replace(' ', '_').lower() for name in raw_data.feature_names]
    )
    dataset['species_class'] = raw_data.target
    
    dataset.to_csv(dataset_output.path, index=False)
