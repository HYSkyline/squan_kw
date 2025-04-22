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
    model="qwen-plus",  # 可按需更换模型名称
    messages=[
        {'role': 'system', 'content': '返回类似{"question":"answer"}形式的json结果'},
        {'role': 'user', 'content': '请介绍一下明朝的空印案'}
    ],
    stream=True,
    response_format={"type": "json_object"},
    extra_body={"enable_search": True},
)

full_content = ''
# 通过content字段打印最终答案
print("最终答案：")
for chunk in completion:
    # 如果stream_options.include_usage为True，则最后一个chunk的choices字段为空列表，需要跳过（可以通过chunk.usage获取 Token 使用量）
    if chunk.choices:
        full_content += chunk.choices[0].delta.content
        print(chunk.choices[0].delta.content, end='')
# print(f"\n完整内容为：{full_content}")
