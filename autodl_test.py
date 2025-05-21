# -*- coding:utf-8 -*-

from openai import OpenAI


with open('config.config', 'r') as f_ip:
    content = f_ip.readlines()
autodl_ip = content[2].split(',')[1][:-1]  # 实际使用时，IP 替换为 Ollama 所在的服务器 IP
autodl_model = content[3].split(':')[1][:-1]
autodl_key = content[4].split(':')[1][:-1]

client = OpenAI(
    api_key=autodl_key,
    base_url=autodl_ip,
)
chat_response = client.chat.completions.create(
    model=autodl_model,
    messages=[
        {'role': 'system', 'content': '返回类似{"question":"answer"}形式的json结果'},
        {'role': 'user', 'content': '请简单介绍一下明朝的空印案'}
    ],
    stream=False,
    max_tokens=32768,
    temperature=0.6,
    top_p=0.95,
    extra_body={
        "top_k": 20,
    },
    response_format={"type": "json_object"},
)
print("Chat response content:\n" + chat_response.choices[0].message.reasoning_content)


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