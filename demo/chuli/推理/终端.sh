#!/bin/bash
source activate py310_chat

MODEL_PATH="/root/autodl-tmp/glm-4-9b-chat"
TARGET_DIR="/root/autodl-tmp"
THRESHOLD=30000000  # 剩余空间的阈值，单位为KB，即30GB

# 检查剩余磁盘空间
available_space=$(df "$TARGET_DIR" | awk 'NR==2 {print $4}')

# 检查模型文件夹是否存在
if [ -d "$MODEL_PATH" ]; then
    echo "发现已有glm-4-9b-chat模型文件，直接运行推理程序。"
    python /root/GLM-4/basic_demo/trans_cli_demo.py
    echo "程序已退出。"
    exit 0
fi

# 如果模型文件夹不存在，检查剩余磁盘空间
if [ "$available_space" -lt "$THRESHOLD" ]; then
    echo "你好，发现您autodl-tmp 磁盘下的空余内存不足。需要我为您清空吗？输入：yes 或者 no"
    read user_input
    if [ "$user_input" = "yes" ]; then
        if rm -rf "$TARGET_DIR"/*; then
            echo "磁盘已清空。"
        else
            echo "清空磁盘失败。"
            exit 1
        fi
    else
        echo "程序已退出。"
        exit 0
    fi
fi

# 下载模型文件并运行推理程序
echo "你好！发现您并没有glm-4-9b-chat模型文件，需要我为您下载吗？输入：yes 或者 no"
read user_input
if [ "$user_input" = "yes" ]; then
    cd "$TARGET_DIR"
    if cg down xxxiu/glm-4-9b-chat; then
        python /root/GLM-4/basic_demo/trans_cli_demo.py
    else
        echo "下载模型失败。"
        exit 1
    fi
else
    echo "程序已退出。"
    exit 0
fi

echo "程序已退出。"
exit 0


