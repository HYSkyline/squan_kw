# -*- coding:utf-8 -*-

import time
import os
import requests
from docx import Document


def main(f_path):
    print('Start.')
    print('--' * 6)

    txt_content = format_trans(f_path)
    # print(u'******调试用********\n' + txt_content)
    data_res = data_extract(txt_content)
    output_check = data_output(data_res)

    print(u'EOF.')


def format_trans(file_path):
    print(u'对输入文件进行预处理...')
    file_all_name = os.path.split(file_path)[1]
    file_name, file_format = file_all_name.split('.')
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
    return content


def data_extract(txt_content):
    print(u'文字信息正在提交大模型...')
    with open('local_ollama_ip.config', 'r') as f_ip:
        ollama_ips = f_ip.readlines()

    prompt_pre = u'请提取以下内容中的指标名称和数据，并将其整理成表格形式。不可对文字进行修改，不可对数据进行修改，不可对指标和数据的对应关系进行篡改。\
    需要提取数据的内容如下：\n'
    url = "http://" + ollama_ips[1][:-1] + ":11434/api/generate"  # 实际使用时，IP 替换为 Ollama 所在的服务器 IP
    payload = {
        "model": "qwq:32b",
        "prompt": prompt_pre + txt_content,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        if response.ok:
            print(u"已由大模型处理完成.\n" + '--' * 6)
            return response.text
        else:
            print(f"大模型处理失败，状态码：{response.status_code}，程序即将退出.")
            exit()
    except Exception as e:
        print(e)
        exit()


def data_output(res):
    print(u'数据抽取结果保存中....')
    with open(u'公报数据抽取测试.txt', 'w', encoding='utf-8') as f_res:
        for each in res:
            f_res.writelines(each)
    print(u'数据抽取结果已保存.\n' + '--' * 6)
    return 200


def file_read_txt(f_path):
    try:
        with open(f_path, 'r', encoding='gbk') as f_data:
            content = f_data.read()
        return content.replace('\n\n', '\n').replace('  ', ' ')
    except UnicodeDecodeError as e:
        with open(f_path, 'r', encoding='utf-8') as f_data:
            content = f_data.read()
        return content.replace('\n\n', '\n').replace('  ', ' ')
    else:
        print(u'txt的编码格式不正确，建议更换源文件格式或重新从网页上下载txt文件.')


def file_read_html(f_path):
    return ''


def file_read_docx(f_path):
    return ''


def file_read_pdf(f_path):
    return ''


if __name__ == '__main__':
    # f_path = 'https://www.ly.gov.cn/2024/05-09/144721.html'
    f_path = u'C:\\项目文件\\squan_kw\\2023年洛阳市国民经济和社会发展统计公报.txt'
    main(f_path)
