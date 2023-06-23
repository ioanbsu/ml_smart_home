#!/usr/bin/env sh
#executing: ./nuke_and_setup_from_scratch.sh env_name
# replace env_name with env name of your choice.
env_name=$1
resolved_env=${env_name:-m1_gpu_env}

# If you're seeing issues installing som eof packages, your conda env might have cached files that may worth cleaning up
# uncomment line below if this is the case.
#conda clean --all
conda update conda
conda update python
conda deactivate
conda env remove -n ${resolved_env}
conda env create -f tf-metal-arm64.yaml -n ${resolved_env}
conda init zsh


echo "Conda env setup completed. To activate your environment run \`conda activate ${resolved_env}\`"
echo "once activating the env, run following cmds: "
echo "pip install numpy  --upgrade"
echo "pip install pandas  --upgrade"
echo "pip install matplotlib  --upgrade"
echo "pip install scikit-learn  --upgrade"
echo "pip install scipy  --upgrade"
echo "pip install plotly  --upgrade"
echo "pip install ultralytics  --upgrade"

