# -*- coding:utf-8 -*-

from markitdown import MarkItDown
import time
import os
import requests
from pdf2docx import Converter


def main(file_list):
	print('Link Start!')
	print('--' * 6)
	time_ori = time.time()

	# word文件转md
	md_word = file_trans(file_list['word'])
	with open('temp/md_res_word.txt', 'w', encoding='utf-8') as f_res:
		f_res.write(md_word)
	print('word file converted.')

	# PDF文件先转word再转md
	cv = Converter(file_list['pdf'])
	cv.convert('temp/md_tmp_pdf.docx')
	cv.close()
	md_pdf = file_trans('temp/md_tmp_pdf.docx')
	with open('temp/md_res_pdf.txt', 'w', encoding='utf-8') as f_res:
		f_res.write(md_pdf)
	print('pdf file converted.')

	# HTML文件打开网页转md
	md_html = file_trans(requests.get(file_list['html']))
	with open('temp/md_res_html.txt', 'w', encoding='utf-8') as f_res:
		f_res.write(md_html)
	print('html file converted.')
	print('--' * 6)

	print('Time escape:' + str(int((time.time() - time_ori) * 100) / 100) + 's.')
	print('Link Logout.')


def file_trans(f_o):
	md = MarkItDown()
	res = md.convert(f_o).text_content
	return res


if __name__ == '__main__':
	file_list = {
		'word': u'material/md素材-2023年洛阳市国民经济和社会发展统计公报.docx',
		'pdf': u'material/黔东南苗族侗族自治州2023年国民经济和社会发展统计公报.pdf',
		'html': 'https://tjj.qdn.gov.cn/tjsj/tjgb_57099/tjgb_57101/202105/t20210508_68020510.html'
	}
	main(file_list)
