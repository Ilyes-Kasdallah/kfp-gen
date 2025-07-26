
from kfp import pipeline
from kfp.components import load_sales_transactions, batch_predict_pipeline

@pipeline(name="CLV Batch Predict")
def CLV_Batch_Predict():
    # Load sales transactions data from GCS
    load_sales_transactions()
    
    # Batch predict CLV
    batch_predict_pipeline()

# Define the components
load_sales_transactions = load_sales_transactions()
batch_predict_pipeline = batch_predict_pipeline()

# Execute the pipeline
CLV_Batch_Predict()
