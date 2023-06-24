# Machine Learning meets smart home (home assistant)

In this repository you'll find necessary instructions to train CV model and deploy it so that it can send events to
smart home system trough MQTT.


## Prerequisites

1. **Mac M1**
1. **conda/miniconda**
1. **Home Assistant (HA) installed**. While this approach will very likely to work with other smart home solutions, we will be using home
   assistant in this example. You are more than welcome to try to adopt proposed here solution to different smart home
   solutions, but using it with home assistant will make following staps in this instruction a lot easier.  
1. **MQTT - installed and integrated with HA**
1. **Python**
1. **Docker**
1. **Grafana(optional)**


## Plan
1. Env setup
   1. Install docker (google it)
   1. Install conda (google it). Miniconda will work as well
   1. Init conda env and attach it to IDEA
   1. Link conda env to jupiter notebook: `python -m ipykernel install --user --name ml_smart_home --display-name "ML Smart Home"`
1. Labeling - recorded
   1. Start label-studio. Create account, get ready to import
   1. Record images to train on
   1. Upload images
   1. Label Images
1. Training - recorded
   1. Splitting dataset into training and validating
   1. Training using yolov8x
1. Testing
   1. Using provided python script, test that objects detedction works as expected.
1. Home automation integration
   1. Home automation software: Home Assistant
   1. Integration point: mqtt
   1. Understanding python code that does object detection
   1. Understanding python code that generates mqtt messages 

## Starting image labeling software: label-studio
The label studio is a convenient software that allows labeling ML datasets and exporting them in different formats. You can start local version of it using docker:
```shell
docker-compose up
```
Once it successfully started, the label-studio should be available under http://localhost:18888/

