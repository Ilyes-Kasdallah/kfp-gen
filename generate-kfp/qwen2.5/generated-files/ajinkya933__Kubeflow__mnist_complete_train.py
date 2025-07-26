
from kfp import dsl

@dsl.pipeline(name="mnist_pipeline")
def mnist_pipeline(data_path, model_file):
    # Load the Fashion MNIST dataset
    from tensorflow.keras.datasets import mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    
    # Normalize the dataset
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    
    # Create a Keras sequential model
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10, activation='softmax')
    ])
    
    # Compile the model
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    # Train the model
    model.fit(x_train, y_train, epochs=10, batch_size=32)
    
    # Save the model
    model.save(model_file)

# Define the function to run the pipeline
@dsl.component
def mnist_complete_train():
    return mnist_pipeline("path/to/data", "path/to/model")

# Example usage
mnist_complete_train().execute()
