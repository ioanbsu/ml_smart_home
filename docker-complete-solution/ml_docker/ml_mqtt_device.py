import argparse
import json
import threading

import cv2
import paho.mqtt.client as mqtt
import yaml
from jinja2 import Template
from ultralytics import YOLO

from yolo_detector import YoloDetector

DETECTION_THRESHOLD = 0.8

# Assuming df is your DataFrame
SENSOR_NAME_TEMPLATE = Template("{{ cam_name }} - {{ label_name }} Computer Vision")
SENSOR_ID_TEMPLATE = Template("{{ cam_name }}_{{ label_name }}_mlcv")
MQTT_SENSOR_CONFIG_PATH = Template("homeassistant/switch/{{ cam_name }}/{{ label_name }}/config")
MQTT_SENSOR_STATE_PATH = Template("homeassistant/switch/{{ cam_name }}/state")
MQTT_SENSOR_COMMAND_PATH = Template("homeassistant/switch/{{ cam_name }}/set")


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default="config.yaml", type=str, help='Path to the config')
    parser.add_argument('--mode', default="prod", type=str,
                        help='Mode to run the script in. If dryrun mode passed, then '
                             'no messages will be published to mqtt. The app will only '
                             'report what topics and messages will be sent to mqtt, but '
                             'wouldn\'t actually post anything.')
    opt = parser.parse_args()
    return opt


def generate_switch_config_payload(camera_name, label_name):
    switch_name = SENSOR_NAME_TEMPLATE.render(cam_name=camera_name, label_name=label_name)
    switch_id = SENSOR_ID_TEMPLATE.render(cam_name=camera_name, label_name=label_name)
    state_mqtt_path = MQTT_SENSOR_STATE_PATH.render(cam_name=camera_name)
    command_mqtt_path = MQTT_SENSOR_COMMAND_PATH.render(cam_name=camera_name)
    config_payload_json = {
        "object_id": switch_id,
        "name": switch_name,
        "state_topic": state_mqtt_path,
        "command_topic": command_mqtt_path,
        "value_template": "{{ value_json." + label_name + " }}"
    }
    return config_payload_json


def generate_sensor_config(camera_name, label_name, mqtt_client):
    # create topic for arbitrary number sensor
    sensor_config_payload = generate_switch_config_payload(camera_name, label_name)
    sensor_config_topic = MQTT_SENSOR_CONFIG_PATH.render(cam_name=camera_name, label_name=label_name)
    publish_to_mqtt(sensor_config_topic, json.dumps(sensor_config_payload), mqtt_client, retain=True)


def publish_to_mqtt(topic, payload, mqtt_client, retain=False):
    print("Publishing. Topic: ", topic, "Payload: ", payload)
    if args.mode != 'dryrun':
        mqtt_client.publish(topic, payload, retain=retain, qos=1)


class RTSPStream:
    def __init__(self, rtsp_url):
        self.capture = cv2.VideoCapture(rtsp_url)
        self.frame = None
        self.is_reading = False
        self.thread = threading.Thread(target=self._read_frames)

    def start(self):
        self.is_reading = True
        self.thread.start()

    def stop(self):
        self.is_reading = False
        self.thread.join()

    def _read_frames(self):
        while self.is_reading:
            ret, frame = self.capture.read()
            if ret:
                self.frame = frame

    def get_latest_frame(self):
        return self.frame




args = parse_opt()
# Read the YAML file
with open(args.config, 'r') as file:
    yaml_data = file.read()
# Deserialize the YAML data into a Python object
parsed_yaml = yaml.safe_load(yaml_data)

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(parsed_yaml['mqtt_broker_login'], parsed_yaml['mqtt_broker_password'])
mqtt_client.connect(parsed_yaml['mqtt_broker_host'], parsed_yaml['mqtt_broker_port'])
mqtt_client.loop_start()

print(parsed_yaml['yolo_weights'])
video_detection_model = YOLO(parsed_yaml['yolo_weights'])
model_labels_dict = video_detection_model.model.names
cameras = parsed_yaml['cameras']

width, height = 1280, 720
captures = {}
# generating all sensors configs based on provided cameras and model's labels/classes and publishing their configuration to mqtt
for camera_name in cameras:
    print("Setting up camera: ", cameras[camera_name])
    cap = cv2.VideoCapture(cameras[camera_name]['url'])
    cap.set(3, width)
    cap.set(4, height)
    captures[camera_name] = cap
    for switch in cameras[camera_name]['switches']:
        generate_sensor_config(camera_name, switch, mqtt_client=mqtt_client)

states_map = {}
yolo_detector = YoloDetector(parsed_yaml['yolo_weights'])
while True:
    for camera_name in cameras:
        cap = captures[camera_name]
        success, img = cap.read()
        if success:
            detections_map = yolo_detector.detect(img)
            for switch_payload in detections_map:
                topic = MQTT_SENSOR_STATE_PATH.render(cam_name=camera_name)
                payload = json.dumps(switch_payload)
                if topic not in states_map or states_map[topic] != payload:
                    publish_to_mqtt(MQTT_SENSOR_STATE_PATH.render(cam_name=camera_name), json.dumps(switch_payload),
                                    mqtt_client=mqtt_client)
                    states_map[topic] = payload

mqtt_client.loop_stop()
mqtt_client.disconnect()
