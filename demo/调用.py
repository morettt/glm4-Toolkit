import requests
import json

def send_message(prompt, history):
    url = "http://0.0.0.0:6006"
    headers = {'Content-Type': 'application/json'}
    data = {
        "prompt": prompt,
        "history": history
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Received status code {response.status_code}")
        return None

def main():
    # 定义一个系统消息，作为上下文的一部分
    system_message = {"role": "system", "content": "你是一个聪明的AI"}
    # 初始化历史记录并添加系统消息
    history = [system_message]
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Exiting conversation.")
            break
        response_data = send_message(user_input, history)
        if response_data:
            print("AI:", response_data['response'])
            # 维护历史记录，包括用户输入和AI响应
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response_data['response']})

if __name__ == "__main__":
    main()
