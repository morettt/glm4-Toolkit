import json

def process_and_transform_file(input_path, output_path):
    try:
        # 存储所有对话块
        dialogue_blocks = []
        # 当前处理的对话块
        current_dialogue = []

        with open(input_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line == "":  # 空行表示一个对话块的结束
                    if current_dialogue:
                        dialogue_blocks.append({"messages": current_dialogue})
                        current_dialogue = []  # 重置对话块
                    continue

                # 解析用户或模型发言
                if line.startswith(("用户：", "用户:")):
                    current_dialogue.append({"role": "user", "content": line[3:].strip()})
                elif line.startswith(("模型：", "模型:")):
                    current_dialogue.append({"role": "assistant", "content": line[3:].strip()})

        # 确保文件末尾的对话块也被添加
        if current_dialogue:
            dialogue_blocks.append({"messages": current_dialogue})

        with open(output_path, 'w', encoding='utf-8') as output_file:
            for entry in dialogue_blocks:
                output_file.write(json.dumps(entry, ensure_ascii=False) + '\n')

        print(f"转换完成，并已保存至：{output_path}")

    except Exception as e:
        print(f"处理文件时发生错误：{e}")

# 指定原始文件路径和输出文件路径
input_path = "/root/chuli/微调/多轮对话微调/新文件.txt"
output_path = "/root/GLM-4/finetune_demo/data/train.jsonl"

# 调用函数处理文件
process_and_transform_file(input_path, output_path)
