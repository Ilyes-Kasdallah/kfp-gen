
from kfp import dsl

@dsl.pipeline(name="train_until_good_pipeline")
def train_until_good_pipeline(
    xgb_model_path: str,
    data_path: str,
    error_threshold: float,
    num_epochs: int = 10,
    batch_size: int = 32,
    num_workers: int = 4,
    max_batch_size: int = 1024,
    seed: int = 42,
):
    # Load data
    df = pd.read_csv(data_path)
    
    # Split data into training and validation sets
    train_df, val_df = df.sample(frac=0.8, random_state=seed), df.sample(frac=0.2, random_state=seed)
    
    # Train XGBoost model
    model = xgb.XGBRegressor(
        learning_rate=0.05,
        n_estimators=num_estimators,
        max_depth=3,
        min_child_weight=0.01,
        subsample=0.8,
        colsample_bytree=0.8,
        objective='binary:logistic',
        eval_metric='rmse',
        n_jobs=num_workers,
        random_state=seed,
    )
    model.fit(train_df, label=train_df['target'])
    
    # Evaluate model on validation set
    val_preds = model.predict(val_df)
    val_rmse = np.sqrt(mean_squared_error(val_df['target'], val_preds))
    
    # Check if model has converged
    if val_rmse < error_threshold:
        print("Model converged after", num_epochs, "epochs.")
        return model
    
    # Recursive training
    return recursive_training(xgb_model_path, data_path, error_threshold, num_epochs, batch_size, num_workers, max_batch_size, seed)

# Example usage
xgb_model_path = "path/to/xgb_model"
data_path = "path/to/data.csv"
error_threshold = 0.01
num_epochs = 10
batch_size = 32
num_workers = 4
max_batch_size = 1024
seed = 42

model = train_until_good_pipeline(
    xgb_model_path,
    data_path,
    error_threshold,
    num_epochs,
    batch_size,
    num_workers,
    max_batch_size,
    seed,
)
