import json
from tensorflow.keras.callbacks import Callback


class MetricsCollector(Callback):
    """
    A callback class for collecting and exporting model training metrics to a JSON file.

    Usage:
    Instantiate the class and use it as a callback during model training to collect metrics after each epoch.
    Call the `export_to_json` method to export the collected metrics to a JSON file.
    Note: on_epoch_end() method is called by Keras at the end of each epoch (it is overridden).
    This method collects the training metrics and it is called automatically during model training.

    Example:
    ```python
    from experiment_tracker.metrics_collector import MetricsCollector
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense

    # Define a Keras model
    model = Sequential([
        Dense(64, activation='relu', input_shape=(10,)),
        Dense(1, activation='sigmoid')
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Create an instance of MetricsCollector
    metrics_collector = MetricsCollector()

    # Train the model with MetricsCollector as a callback
    history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_val, y_val), callbacks=[metrics_collector])

    # Export the collected metrics to a JSON file
    metrics_collector.export_to_json("metrics.json")
    ```

    Attributes:
        None

    Methods:
        export_to_json(filename="results.json"):
            Exports the collected training metrics to a JSON file.

    """

    def __init__(self):
        super(MetricsCollector, self).__init__()
        self.losses = []
        self.accuracies = []
        self.val_losses = []
        self.val_accuracies = []

    def on_epoch_end(self, epoch, logs=None):
        self.losses.append(logs["loss"])
        self.accuracies.append(logs["accuracy"])
        self.val_losses.append(logs["val_loss"])
        self.val_accuracies.append(logs["val_accuracy"])

    def export_to_json(self, filename="results.json"):
        """
        Exports the collected training metrics to a JSON file.

        :param str filename: The filename to save the JSON file. (Default: "results.json")
        """
        metrics_dict = {
            "training_loss": self.losses,
            "training_accuracy": self.accuracies,
            "validation_loss": self.val_losses,
            "validation_accuracy": self.val_accuracies,
        }
        with open(filename, "w") as f:
            json.dump(metrics_dict, f)


# Imports for ModelVisualizer
from keras.utils.vis_utils import plot_model


class ModelVisualizer:
    """
    A utility class for visualizing the architecture of Keras models.

    Usage:
    Instantiate the class and call the static method `visualize_model` to generate
    and save a visualization of a Keras model's architecture.

    Example:
    ```python
    from experiment_tracker.model.model_visualizer import ModelVisualizer
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense

    # Define a Keras model
    model = Sequential([
        Dense(64, activation='relu', input_shape=(10,)),
        Dense(1, activation='sigmoid')
    ])

    # Visualize the model and save the plot to a file
    ModelVisualizer.visualize_model(model, 'model_plot.png')
    ```

    Attributes:
        None

    Methods:
        visualize_model(model, plot_filename):
            Generates a visualization of the architecture of a Keras model and saves it to a file.

    """

    @staticmethod
    def visualize_model(model, plot_filename="result.png"):
        """
        Generates a visualization of the architecture of a Keras model and saves it to a file.

        Parameters:
            model (tensorflow.keras.Model): The Keras model to visualize.
            plot_filename (str): The filename to save the plot.

        Raises:
            ValueError: If the provided model is not a Keras model instance.
        """

        plot_model(
            model, to_file=plot_filename, show_shapes=True, show_layer_names=True
        )