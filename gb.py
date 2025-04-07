# -*- coding:utf-8 -*-

import time
import os
import urllib
import ollama

def main():
    pass


def format_trans(file_path):
    file_all_name = os.path.split(file_path)[1]
    file_name, file_format = file_all_name.split('.')
    if file_format == 'html':
        print(u'输入为网页文件，即将联网打开该网页')
    elif file_format == 'docx' or file_format == 'doc':
        print(u'输入为Word文件')
    elif file_format == 'txt':
        print(u'输入为txt文件')
    elif file_format == 'pdf':
        print(u'输入为PDF文件，正在检查是否需要OCR扫描读取文字信息')
    else:
        print(u'还未想好怎么处理的文件格式')
# https://www.ly.gov.cn/2024/05-09/144721.html

if __name__ == '__main__':
    main()
