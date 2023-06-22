import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

class KerasDetector:
    def __init__(self, model_path):
        self.loaded_model = load_model(model_path)
        self.label_mapping = {0: 'SwitchOn', 1: 'SwitchOff'}

    def detect(self, image):
        detections_map = []
        image = img_to_array(image) / 255.0
        # plt.imshow(image)
        image = np.expand_dims(image, axis=0)
        resized_image = tf.image.resize(image, [224, 224])
        predictions = self.loaded_model.predict(resized_image)
        max_probability = 0
        label_with_max_probability = ''

        for i in range(len(self.label_mapping)):
            print("{}".format(self.label_mapping[i]), " {}%".format(predictions[0][i]*100))
            label_name = self.label_mapping[i]
            probability = predictions[0][i] * 100
            if probability > max_probability:
                label_with_max_probability = label_name
                max_probability = probability
        detection = {}
        switch_state = 'undefined'
        if label_with_max_probability.endswith('On'):
            switch_state = 'ON'
        if label_with_max_probability.endswith('Off'):
            switch_state = 'OFF'

        switch_name = label_with_max_probability.replace('On', '').replace('Off', '')
        detection[switch_name] = switch_state
        detections_map.append(detection)
        return detections_map
