import os
import torch
from threading import Thread
from transformers import (
    AutoTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
    TextIteratorStreamer, AutoModel, BitsAndBytesConfig
)

from PIL import Image

MODEL_PATH = os.environ.get('MODEL_PATH', '/root/autodl-tmp/glm-4v-9b')
IMAGE_DIR = '/root/GLM-4/图片存放'

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    trust_remote_code=True,
    encode_special_tokens=True
)
model = AutoModel.from_pretrained(
    MODEL_PATH,
    trust_remote_code=True,
    # attn_implementation="flash_attention_2",  # Use Flash Attention
    torch_dtype=torch.bfloat16,
    device_map="auto",
).eval()

## For INT4 inference
# model = AutoModel.from_pretrained(
#     MODEL_PATH,
#     trust_remote_code=True,
#     quantization_config=BitsAndBytesConfig(load_in_4bit=True),
#     torch_dtype=torch.bfloat16,
#     low_cpu_mem_usage=True
# ).eval()

class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        stop_ids = model.config.eos_token_id
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False


if __name__ == "__main__":
    history = []
    max_length = 1024
    top_p = 0.8
    temperature = 0.7
    stop = StopOnTokens()
    uploaded = False
    image = None
    print("请将图片存入左侧“图片存放”文件夹中，且保证是jpg格式，和英文名")
    image_name = input("输入图片名字:")
    image_path = os.path.join(IMAGE_DIR, f"{image_name}.jpg")
    try:
        image = Image.open(image_path).convert("RGB")
    except:
        print("图像路径无效。继续进行文字对话。")
    
    # Add a system message for context initialization
    system_message = {"role": "system", "content": "你是一个人类。模仿专业的分析师和用户对话"}
    history.append([system_message["content"], ""])

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        history.append([user_input, ""])

        messages = []
        for idx, (user_msg, model_msg) in enumerate(history):
            if idx == 0:  # Add the system message at the beginning
                messages.append(system_message)
            if idx == len(history) - 1 and not model_msg:
                messages.append({"role": "user", "content": user_msg})
                if image and not uploaded:
                    messages[-1].update({"image": image})
                    uploaded = True
                break
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if model_msg:
                messages.append({"role": "assistant", "content": model_msg})
        
        model_inputs = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_tensors="pt",
            return_dict=True
        ).to(next(model.parameters()).device)
        streamer = TextIteratorStreamer(
            tokenizer=tokenizer,
            timeout=60,
            skip_prompt=True,
            skip_special_tokens=True
        )
        generate_kwargs = {
            **model_inputs,
            "streamer": streamer,
            "max_new_tokens": max_length,
            "do_sample": True,
            "top_p": top_p,
            "temperature": temperature,
            "stopping_criteria": StoppingCriteriaList([stop]),
            "repetition_penalty": 1.2,
            "eos_token_id": [151329, 151336, 151338],
        }
        t = Thread(target=model.generate, kwargs=generate_kwargs)
        t.start()
        print("GLM-4V:", end="", flush=True)
        for new_token in streamer:
            if new_token:
                print(new_token, end="", flush=True)
                history[-1][1] += new_token

        history[-1][1] = history[-1][1].strip()
