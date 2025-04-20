import tensorflow as tf
from tensorflow.keras import layers, models, optimizers

"""
Parameters:
- input_shape (tuple): Shape of the input features (e.g., (10,) for 10 features).
- output_classes (int): Number of output classes (e.g., 3 for Navigate, Hover, Land).

Returns:
- model (tf.keras.Model): Compiled TensorFlow model.
"""
def build_advanced_ai_model(input_shape, output_classes):
    model = models.Sequential()

    # Input Layer
    model.add(layers.InputLayer(input_shape=input_shape))

    # Hidden Layers
    model.add(layers.Dense(512, activation='relu', kernel_initializer='he_normal'))
    model.add(layers.Dropout(0.3))  # Dropout for regularization

    model.add(layers.Dense(256, activation='relu', kernel_initializer='he_normal'))
    model.add(layers.Dropout(0.3))

    model.add(layers.Dense(128, activation='relu', kernel_initializer='he_normal'))
    model.add(layers.Dropout(0.2))

    model.add(layers.Dense(64, activation='relu', kernel_initializer='he_normal'))

    # Output Layer
    model.add(layers.Dense(output_classes, activation='softmax'))

    # Compile the model
    model.compile(
        optimizer=optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    print("Advanced AI Model successfully built and compiled.")
    return model

print(tf.__version__)