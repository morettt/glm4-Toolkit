#!/bin/bash
cd /root
source activate py310_chat  

mv /root/glm-4-9b-chat /root/autodl-tmp

python /root/GLM-4/basic_demo/trans_cli_demo.py

