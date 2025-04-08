# -*- coding:utf-8 -*-

import time
import os
import requests
from openai import OpenAI
# from docx import Document
from markitdown import MarkItDown
import re
import json


def main(f_path):
    print('Start.')
    print('--' * 6)
    print(u'当前时间：' + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    time_origin = time.time()

    txt_content = format_trans(f_path)
    # print(u'******调试用********\n' + txt_content[-1])
    for i in range(1, len(txt_content)):
        time_para = time.time()
        para_name = txt_content[i][:txt_content[i].find('\n')]
        print(u'文字信息正在提交大模型. 当前章节:' + para_name)
        # data_res = data_extract_ollama(txt_content[i])
        # output_check = data_output_ollama(para_name, data_res)
        data_res = data_extract_aliyun(txt_content[i])
        output_check = data_output_aliyun(para_name, data_res)
        print(u'本篇章数据已提取。共耗时:' + str(int((time.time() - time_para) * 100) / 100) + 's.')
        print('--' * 6)
        time.sleep(1)
    print(u'\n总计耗时:' + str(int((time.time() - time_origin) * 100) / 100) + 's.\n程序已完成.')


def format_trans(file_path):
    print(u'对输入文件进行预处理...')
    file_all_name = os.path.split(file_path)[1]
    file_name, file_format = file_all_name.split('.')
    content = ''

    if file_format == 'html':
        print(u'网址: ' + file_name)
        print(u'待处理文件为网页文件，即将联网打开该网页')
        content = file_read_html(file_path)
    elif file_format == 'docx' or file_format == 'doc':
        print(u'文件名:' + file_name)
        print(u'待处理文件为Word文件，已直接读取')
        content = file_read_docx(file_path)
    elif file_format == 'txt':
        print(u'文件名:' + file_name)
        print(u'待处理文件为txt文件，已直接读取')
        content = file_read_txt(file_path)
    elif file_format == 'pdf':
        print(u'文件名:' + file_name)
        print(u'待处理文件为PDF文件，正在检查是否需要OCR扫描读取文字信息...')
        content = file_read_pdf(file_path)
    else:
        print(u'还未想好怎么处理的文件格式')

    print('--' * 6)
    content_paras = content_split(content)
    return content_paras


def data_extract_ollama(txt_content):
    with open('local_ollama_ip.config', 'r') as f_ip:
        ollama_ips = f_ip.readlines()
    with open('prompt_pre.txt', 'r', encoding='utf-8') as f_prompt:
        prompt_pre = f_prompt.read()
    # print(u'*******调试用*******\n' + prompt_pre + txt_content.replace(' ', '') + '\n******************')
    url = "http://" + ollama_ips[0][:-1] + ":11434/api/generate"  # 实际使用时，IP 替换为 Ollama 所在的服务器 IP
    payload = {
        "model": "qwq:latest",
        "prompt": prompt_pre + txt_content,
        "options": {
            "temperature": 0,
            # "max_tokens": 500,
            # "top_p": 0.9,
            # "num_ctx": 0,
        },
        "stream": False,
        "format": "json",
    }

    try:
        response = requests.post(url, json=payload)
        if response.ok:
            # print(u"已由大模型处理完成.\n" + '--' * 6)
            return response.text
        else:
            print(f"大模型处理失败，状态码：{response.status_code}，程序即将退出.")
            exit()
    except Exception as e:
        print(e)
        exit()


def data_extract_aliyun(txt_content):
    with open('prompt_pre.txt', 'r', encoding='utf-8') as f_prompt:
        prompt_pre = f_prompt.read()

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
            {'role': 'user', 'content': prompt_pre + txt_content}
        ]
    )
    return completion.choices[0].message.content


def data_output_ollama(para_name, res):
    res_json = json.loads(res)['response'].replace('\n', '').replace(' ', '')
    with open(u'公报数据抽取测试-' + para_name + '.txt', 'w', encoding='utf-8') as f_res:
        f_res.write(res_json)
    # print(u'数据抽取结果已保存.\n' + '--' * 6)
    return 200


def data_output_aliyun(para_name, res):
    with open(u'公报数据抽取测试-' + para_name + '.txt', 'w', encoding='utf-8') as f_res:
        f_res.write(res)
    # print(u'数据抽取结果已保存.\n' + '--' * 6)
    return 200
    

def file_read_txt(f_path):
    try:
        with open(f_path, 'r', encoding='gbk') as f_data:
            content = f_data.read()
        return content
    except UnicodeDecodeError as e:
        with open(f_path, 'r', encoding='utf-8') as f_data:
            content = f_data.read()
        return content
    except Exception as e:
        print(e)


def file_read_html(f_path):
    try:
        response = requests.post(f_path)
        return response.text
    except Exception as e:
        print(u'网页读取失败:' + str(e))
        exit()


def file_read_docx(f_path):
    md = MarkItDown()
    result = md.convert(f_path)
    return result.text_content


def file_read_pdf(f_path):
    md = MarkItDown()
    result = md.convert(f_path)
    return result.text_content


def content_split(txt):
    para_index = [s for s in re.split(r'[一二三四五六七八九十]+、', txt) if s]
    # print(u'******调试用********\n' + str(len(para_index)))
    # for each in para_index:
    #     print(each)
    #     print('***' * 6)
    return para_index


if __name__ == '__main__':
    # f_path = 'https://www.ly.gov.cn/2024/05-09/144721.html'
    f_path = u'D:\\squan_kw\\2023年洛阳市国民经济和社会发展统计公报.txt'
    global time_origin
    main(f_path)
