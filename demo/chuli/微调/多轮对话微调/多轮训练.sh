#!/bin/bash

source activate py310_chat     
cd /root/GLM-4/finetune_demo
python finetune.py  data  /root/autodl-tmp/glm-4-9b-chat  configs/lora.yaml