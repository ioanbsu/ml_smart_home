# Machine Learning meets smart home (home assistant): ML-Switch

In this repository you'll find code that allows to train Computer Vision (CV) Machine Learning(ML) model and generate
MQTT events that are recognized by Home Assistant as MQTT Switch.

## Prerequisites

1. **Mac M1**
1. **conda/miniconda**
1. **Docker**
1. **Home Assistant (HA) installed**. While this approach will very likely to work with other smart home solutions, we
   will be using home
   assistant in this example. You are more than welcome to try to adopt proposed here solution to different smart home
   solutions, but using it with home assistant will make following staps in this instruction a lot easier.
1. **MQTT - installed and integrated with HA**
1. **Python**
1. **Grafana(optional)**

## Plan

1. Labeling
    - Start label-studio. Create account, get ready to import
    - Record images to train on
    - Upload images
    - Label images
    - Export images
1. Training
    - Splitting dataset into training, validating and test. [Here](https://blog.roboflow.com/train-test-split/) is a
      very good explanation why that is needed.
    - Training using yolov8x
1. Env setup
    - Install docker (google it)
    - Install conda (google it). Miniconda will work just fine well
    - Setup conda env in IDEA
    - Init conda env and "attach" it to IDEA
    - Link conda env to jupiter
      notebook: `python -m ipykernel install --user --name ml_smart_home --display-name "ML Smart Home"`. This step is
      optional but is recommended, you can just run all commands from cmd line provided you ruin them from appropriate
      conda environment.
1. Testing
    - Using provided yolo_predict_test.py python script, test that objects detection works as expected
1. Home automation integration
    - Home automation
      software: [Home Assistant + mqtt + docker slides](https://docs.google.com/presentation/d/1mjaZtqBLXoZ5ldYte4zNezX3tK09N_yNoPJBgD8XVoI/edit?usp=sharing).
1. All-in-one-docker integration.
    - All in one docker file available at `docker-complete-solution`. To start it
      run: `cd docker-complete-solution; docker-compose up`
    - The python code that does object detection and pushing mqtt messages is
      at `docker-complete-solution/ml_docker/ml_mqtt-device.py`

## Step by step instructions

For complete step-by step instructions check out [youtube video](https://youtu.be/4ETaWTp7LQA) 

