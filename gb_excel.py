# -*- coding:utf-8 -*-

import os
import time
import json
import xlwt


print('Link Start!')
time_start = time.time()
f_list = []
for each in os.listdir(os.getcwd() + '\\data'):
    if 'aliyun' in each:
        f_list.append(each)

index_list = []
for each in f_list:
    with open('data/' + each, 'r', encoding='utf-8') as f_json:
        cont = f_json.readlines()[1:-1]
    for index in json.loads(''.join(cont).replace('\n','')):
        index_list.append(index)

keys = sorted({key for item in index_list for key in item.keys()})

# 创建Excel工作簿和工作表
workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet('Data')

# 写入列名（首行）
for col_idx, key in enumerate(keys):
    worksheet.write(0, col_idx, key)

# 写入数据行
for row_idx, item in enumerate(index_list, 1):  # 从第1行开始（Excel第二行）
    for col_idx, key in enumerate(keys):
        value = item.get(key, '')  # 处理缺失键，默认为空字符串
        worksheet.write(row_idx, col_idx, value)

# 保存Excel文件
workbook.save('data/aliyun.xls')