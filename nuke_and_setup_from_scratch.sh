#!/usr/bin/env sh
#executing: ./full_env_reset.sh env_name
# replace env_name with env name of your choice.
env_name=$1
resolved_env=${env_name:-m1_gpu_env}

conda deactivate
conda env remove -n ${resolved_env}
conda env create -f tf-metal-arm64.yaml -n ${resolved_env}
conda init zsh


echo "Conda env setup completed. To activate your environment run `conda activate ${resolved_env}`"
echo "once activating the env, run following cmds: "
echo "pip install numpy  --upgrade"
echo "pip install pandas  --upgrade"
echo "pip install matplotlib  --upgrade"
echo "pip install scikit-learn  --upgrade"
echo "pip install scipy  --upgrade"
echo "pip install plotly  --upgrade"
echo "jupyter-lab"

