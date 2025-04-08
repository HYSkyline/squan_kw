# -*- coding:utf-8 -*-

import time
import os
from openai import OpenAI

time_start = time.time()

with open('config.config', 'r') as f_key:
    api_key = f_key.readlines()[1].split(':')[1][:-1]

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=api_key,  # 如何获取API Key：https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

completion = client.chat.completions.create(
    model="deepseek-r1",  # 此处以 deepseek-r1 为例，可按需更换模型名称。
    messages=[
        {'role': 'user', 'content': '请介绍一下最速降线'}
    ]
)

# 通过reasoning_content字段打印思考过程
print("思考过程：")
print(completion.choices[0].message.reasoning_content)
print('--' * 6)

# 通过content字段打印最终答案
print("最终答案：")
print(completion.choices[0].message.content)
print('--' * 6)
print('总用时:' + str(time.time() - time_start) + 's.')
