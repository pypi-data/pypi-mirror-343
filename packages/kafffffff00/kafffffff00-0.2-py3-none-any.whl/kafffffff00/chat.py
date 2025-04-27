# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 16:58:05 2025

@author: pang7
"""

import requests
import time

def start_deepseek_chat(
    model_name: str = 'deepseek-chat',
    base_url: str = 'https://api.deepseek.com/v1',
    save_chat: bool = False,
    save_path: str = 'chat_history.txt'
):
    """
    启动 DeepSeek 连续对话（API密钥已内置）
    参数:
        model_name: 使用的模型，默认 'deepseek-chat'
        base_url: DeepSeek API基础URL
        save_chat: 是否保存聊天记录，默认False
        save_path: 聊天记录保存路径
    """
    # 在这里直接写死 API Key
    api_key = 'sk-2c8d4f8c45994385bf06fc231a117009'

    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    print(f"欢迎使用 DeepSeek 聊天模式！输入 'exit' 或 '退出' 可结束对话。\n当前使用模型: {model_name}")

    while True:
        user_input = input("\n你：")
        if user_input.lower() in ["exit", "退出"]:
            print("对话结束！")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                "model": model_name,
                "messages": messages
            }
            response = requests.post(f'{base_url}/chat/completions', headers=headers, json=data)
            if response.status_code != 200:
                raise Exception(f"API调用失败，状态码: {response.status_code}, 错误信息: {response.text}")

            reply = response.json()["choices"][0]["message"]["content"]
            print("\nDeepSeek：", reply)

            messages.append({"role": "assistant", "content": reply})

            if save_chat:
                with open(save_path, 'a', encoding='utf-8') as f:
                    f.write(f"你: {user_input}\n")
                    f.write(f"DeepSeek: {reply}\n\n")

            time.sleep(0.5)

        except Exception as e:
            print("出错了：", e)
            break
