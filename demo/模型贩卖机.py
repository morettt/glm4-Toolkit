import subprocess
import os
import shutil

def get_free_space_gb(directory):
    """获取指定目录的剩余空间（单位为GB）"""
    total, used, free = shutil.disk_usage(directory)
    return free // (2**30)  # 从字节转换为GB

def clear_directory(directory):
    """清空指定目录"""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def download_model():
    download_path = "/root/autodl-tmp"
    # 确保下载目录存在
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # 检查剩余空间
    free_space_gb = get_free_space_gb(download_path)
    if free_space_gb < 30:
        print(f"剩余空间不足（仅剩 {free_space_gb} GB），正在清空目录...")
        clear_directory(download_path)

    model_name = input("请输入模型名称（如 GLM-4-9B-Chat-1M）：")
    # 特殊模型名称处理
    if model_name == "Qwen-7B-Chat":
        model_name = "Qwen-7B-Chat-new"
    elif model_name == "Llama3-8B-chat":
        model_name = "SmartFlowAI/Meta-Llama3-8B-Instruct"

    os.chdir(download_path)
    command = f"cg down {model_name}"
    print(f"将在 {download_path} 下执行下载命令...")
    subprocess.run(command, shell=True)
    print(f"模型已下载到 {download_path}")

if __name__ == "__main__":
    download_model()
