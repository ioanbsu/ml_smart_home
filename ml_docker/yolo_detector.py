import json
import math

from ultralytics import YOLO


class YoloDetector:
    def __init__(self, model_path):
        self.video_detection_model = YOLO(model_path)

    def detect(self, img):
        detections_map = []
        results = self.video_detection_model.predict(img)
        for result in results:
            bboxes = result.boxes.data
            switch_payload = json.loads('{}')
            switches = {}
            if len(bboxes > 0):
                for bbox in bboxes:
                    label_name = result.names[int(bbox[5].item())]
                    confidence = math.ceil(bbox[4] * 100) / 100
                    # collect sensor data

                    switch_name = 'Switch' #label_name.replace('On', '').replace('Off', '')
                    switch_state = 'undefined'
                    if label_name.endswith('On'):
                        switch_state = 'ON'
                    if label_name.endswith('Off'):
                        switch_state = 'OFF'
                    switch_payload[switch_name] = switch_state
                    detection = {}
                    detection[switch_name] = switch_state
                    detections_map.append(detection)
        return detections_map
