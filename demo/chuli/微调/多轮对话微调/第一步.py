import re

def merge_conversations(conversations):
    merged_conversations = []
    prev_speaker = None
    merged_line = ""

    for line in conversations:
        match = re.match(r"^(用户|模型)[：:]\s*(.+)$", line.strip())  # 修改这里使用 \s* 来匹配任意数量的空格
        if match:
            speaker, content = match.groups()
            if speaker == prev_speaker:
                merged_line += "。" + content
            else:
                if merged_line:
                    merged_conversations.append(f"{prev_speaker}：{merged_line}")
                prev_speaker = speaker
                merged_line = content
        else:
            if merged_line:
                merged_conversations.append(f"{prev_speaker}：{merged_line}")
            merged_conversations.append(line.strip())
            prev_speaker = None
            merged_line = ""

    if merged_line:
        merged_conversations.append(f"{prev_speaker}：{merged_line}")

    return merged_conversations

input_file_path = '/root/GLM-4/数据集全自动处理/多轮对话数据.txt'
output_file_path = '/root/chuli/微调/多轮对话微调/新文件.txt'

# 读取输入文件
with open(input_file_path, 'r', encoding='utf-8') as file:
    conversations = file.readlines()

# 处理对话
merged_conversations = merge_conversations(conversations)

# 将处理后的输出写入新文件
with open(output_file_path, 'w', encoding='utf-8') as file:
    for line in merged_conversations:
        file.write(line + '\n')
