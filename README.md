# Machine Learning meets smart home (home assistant)

In this repository you'll find necessary instructions to train CV model and deploy it so that it can send events to
smart home system trough MQTT.


## Prerequisites

1. **Mac M1**
1. **conda/miniconda**
1. **Docker**
1. **Home Assistant (HA) installed**. While this approach will very likely to work with other smart home solutions, we will be using home
   assistant in this example. You are more than welcome to try to adopt proposed here solution to different smart home
   solutions, but using it with home assistant will make following staps in this instruction a lot easier.  
1. **MQTT - installed and integrated with HA**
1. **Python**
1. **Grafana(optional)**


## Plan
1. Labeling
   1. Start label-studio. Create account, get ready to import
   1. Record images to train on
   1. Upload images
   1. Label Images
1. Training
   1. Splitting dataset into training and validating
   1. Training using yolov8x
1. Env setup
   1. Install docker (google it)
   1. Install conda (google it). Miniconda will work as well
   1. Setup conda env in IDEA
   1. Init conda env and "attach" it to IDEA
   1. Link conda env to jupiter notebook: `python -m ipykernel install --user --name ml_smart_home --display-name "ML Smart Home"`
1. Testing
   1. Using provided python script, test that objects detection works as expected.
1. Home automation integration
   1. Home automation software: Home Assistant
   1. Integration point: mqtt
   1. Understanding python code that does object detection
   1. Understanding python code that generates mqtt messages
1. All-in-one-docker integration.


## Step by step instructions
For complete step-by step instructions check out youtube video: 

