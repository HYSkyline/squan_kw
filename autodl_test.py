# -*- coding:utf-8 -*-

import requests
from openai import OpenAI


with open('config.config', 'r') as f_ip:
    content = f_ip.readlines()
autodl_ip = content[2].split(',')[1][:-1]  # 实际使用时，IP 替换为 Ollama 所在的服务器 IP
autodl_model = content[3].split(':')[1][:-1]

client = OpenAI(
    api_key='EMPTY',
    base_url=autodl_ip,
)
response = client.completions.create(
    model=autodl_model,
    prompt="简要介绍一下最速降线"
)
print(response.json()['text'])




# payload = {
#     "model": autodl_model,  # 只能用qwen3-235b
#     "prompt": u'简要介绍一下最速降线',
#     "options": {
#         "temperature": 0,
#         # "max_tokens": 500,
#         # "top_p": 0.9,
#         # "num_ctx": 0,
#     },
#     "stream": False,
#     # "format": "json",
# }

# try:
#     response = requests.post(autodl_ip, json=payload)
#     if response.ok:
#         print(response.text)
#     else:
#         print(f"大模型处理失败，状态码：{response.status_code}，程序即将退出.")
#         print(response)
#         exit()
# except Exception as e:
#     print(str(e))
#     exit()