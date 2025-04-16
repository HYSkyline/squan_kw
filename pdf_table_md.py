# -*- coding:utf-8 -*-

import json


def main(f_table):
	print('Link Start!')
	print('--' * 6)

	with open(f_table, 'r', encoding='utf-8') as f_t:
		txt = f_t.read()
	md_txt = pdf_table_md(txt)
	with open('temp/pdf_pages/table_md.txt', 'w', encoding='utf-8') as f_md:
		f_md.write(md_txt)
	print('table markdown transformed.')
	print('--' * 6)
	print('Link logout.')


def pdf_table_md(table_txt):
	md = table_txt
	# md = md.replace('\\n', '\n')
	# md = md.replace(']][[', ']],\n[[')
	md = list(md)
	print(md)

	md_txt = ''
	for table in md:
		t_head = table[0]	# ['指标名称', '产量（万吨）', '比上年增长（%）']
		row_num = len(table[1][0].split('\n'))
		data = [t_head, [] * row_num]
		for j in range(len(t_head)):
			t_row = table[1][j]		# '粮食\n#夏粮\n秋粮\n#豆类\n薯类（折粮）\n棉花\n油料\n糖料\n烤烟\n中药材\n蔬菜\n茶叶\n水果（含果用瓜）'
			t_r = t_row.split('\n')
			for i in range(len(t_r)):
				data[i + 1].append(t_r[i])
		for each in data:
			md_txt = md_txt + '|' + '|'.join(each) + '|' + '\n'
	return md_txt


if __name__ == '__main__':
	main('temp/pdf_pages/pdf_table1.txt')
