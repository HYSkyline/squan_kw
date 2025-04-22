# -*- coding:utf-8 -*-

from markitdown import MarkItDown
import time
import os
import requests
import pymupdf
from pdf2docx import Converter


def main(file_list):
	print('Link Start!')
	print('--' * 6)
	time_ori = time.time()

	file_trans_transform(file_list['pdf'], 'temp/md_res_pdf.txt')

	print('--' * 6)
	print('Time escape:' + str(int((time.time() - time_ori) * 100) / 100) + 's.')
	print('Link Logout.')


def file_format_transform(f_input, f_save):
	if not os.path.exists('temp'):
		os.mkdir('temp')
	if not os.path.exists('temp/pdf_pages'):
		os.mkdir('temp/pdf_pages')
	print(u'创建temp文件夹作为缓存文件（运行完成后可手动删除）')

	print(u'对输入文件进行预处理...')
	print('--' * 6)
	format_kind = f_input.split('.')[1]
	if format_kind == 'doc' or format_kind == 'docx':
		print(u'文件名:' + f_input)
		print(u'待处理文件为Word文件，已读取文字及表格')
		return file_trans_docx(f_input, f_save)
	elif format_kind == 'pdf':
		print(u'文件名:' + f_input)
		print(u'待处理文件为PDF文件，已读取文字、解析表格，并保存图表图片（但暂时不支持图表的数据抽取）')
		return file_trans_pdf(f_input, f_save)
	elif format_kind == 'txt':
		print(u'文件名:' + f_input)
		print(u'待处理文件为txt文件，已直接读取')
		return file_trans_txt(f_input, f_save)
	elif format_kind == 'html':
		print(u'网址: ' + f_input)
		print(u'待处理文件为网页文件，正在尝试联网打开...')
		return file_trans_html(f_input, f_save)
	else:
		print(u'文件: ' + f_input)
		print(u'该类型尚未准备预处理程序，不保证结果准确性，建议手动转换为word、txt、html或pdf格式')
		return file_trans_others(f_input, f_save)


def file_trans_docx(f_doc, f_save):
	# 是否考虑把word中的图表jpg保存出来
	md = MarkItDown()
	md_word = md.convert(f_doc).text_content
	with open(f_save, 'w', encoding='utf-8') as f_res:
		f_res.write(md_word)
	print(u'word文件已转换完成')
	return md_word


def file_trans_pdf(f_pdf, f_save):
	# 使用PymuPDF库进行解析，表格解析泛用性差，图表图片提取效果差
	f_p = pymupdf.open(f_pdf)
	full_text = ''
	# with open(f_save, 'wb') as f_res:
	# 	for page in f_p:
	# 		page_text = page.get_text().encode('utf-8')
	# 		full_text = full_text + page_text.decode('utf-8')
	# 		f_res.write(page_text)
	# 		f_res.write(bytes((12,)))
	cv = Converter(f_pdf)
	cv.convert('temp/pdf2word.docx')
	md = MarkItDown()
	md_word = md.convert('temp/pdf2word.docx').text_content
	full_text = md_word + '\n'
	with open('temp/pdf_pages/pdf_table.txt', 'w', encoding='utf-8') as f_tab:
		for page in f_p:
			tabs = page.find_tables()
			if tabs.tables:
				table_md = pdf_table_md(tabs[0].extract())
				f_tab.write(table_md)
				full_text = full_text + table_md
	for page_index in range(1, len(f_p)):
		page = f_p[page_index]
		image_list = page.get_images()
		for image_index, img in enumerate(image_list, start=1):
			xref = img[0]
			pix = pymupdf.Pixmap(f_p, xref)
			if pix.n - pix.alpha > 3:
				pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
			pix.save('temp/pdf_pages/page_%s-image_%s.png' % (page_index, image_index))
			pix = None

	# # 使用pdf2docx库进行格式转换，但表格的指标文字全部都混在一起了，后续不采用
	# cv = Converter(f_pdf)
	# tables = cv.extract_tables()
	# cv.close()
	# f_tab = open('temp/pdf_pages/pdf_table.txt', 'w', encoding='utf-8')
	# for tab in tables:
	# 	f_tab.write(str(tab))

	# # 用markitdown进行解析，但表格直接散架了，后续不采用
	# md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
	# md_pdf = md.convert(f_pdf).text_content
	# with open(f_save, 'w', encoding='utf-8') as f_res:
	# 	f_res.write(md_pdf)
	print(u'pdf文件已转换完成')
	return full_text


def pdf_table_md(table_list):
	md = table_list
	md_txt = ''
	for table in md:
		table = list_none_replace(table)
		if '\n' in table[0]:
			data = [[] for i in range(len(table[0].split('\n')))]
			for j in range(len(table)):
				row = table[j].split('\n')
				for i in range(len(row)):
					data[i].append(row[i])
			for each in data:
				md_txt = md_txt + '|' + '|'.join(each) + '|' + '\n'
		else:
			table = list_none_replace(table)
			md_txt = md_txt + '|' + '|'.join(table) + '|' + '\n'
	return md_txt


def list_none_replace(table):
	for i in range(len(table)):
		if table[i]:
			pass
		else:
			table[i] = ''
	return table


def file_trans_html(f_html, f_save):
	# HTML文件打开网页转md，还需要解决附件下载型的网页
	with open('temp/html_cache.txt', 'w', encoding='utf-8') as f_cache:
		f_cache.write(requests.get(file_list['html']).text_content)
	md = MarkItDown()
	md_html = md.convert('temp/html_cache.txt').text_content
	with open(f_save, 'w', encoding='utf-8') as f_res:
		f_res.write(md_html)
	print(u'html文件已转换完成')
	return md_html


def file_trans_txt(f_txt, f_save):
	md = MarkItDown()
	md_txt = md.convert(f_txt).text_content
	with open(f_save, 'w', encoding='utf-8') as f_res:
		f_res.write(md_html)
	print(u'txt文件已转换完成')
	return md_txt


def file_trans_others(f_input, f_save):
	try:
		md = MarkItDown()
		md_input = md.convert(f_input).text_content
		with open(f_save, 'w', encoding='utf-8') as f_res:
			f_res.write(md_input)
		print(u'输入文件类型不常见，无对应预处理程序，但已经转换完成。需要手动检查数据抽取成果准确性。')
		return md_input
	except Exception as e:
		print(u'输入文件类型超出程序可处理范围 error:' + str(e))
		exit()


def api_key_fetch():
	with open('config.config', 'r') as f_key:
		api_key = f_key.readlines()[1].split(':')[1][:-1]
	os.environ['api_key'] = api_key


if __name__ == '__main__':
	# api_key_fetch()
	file_list = {
		'word': u'material/md素材-2023年洛阳市国民经济和社会发展统计公报.docx',
		'pdf': u'material/黔东南苗族侗族自治州2023年国民经济和社会发展统计公报.pdf',
		'html': 'https://tjj.qdn.gov.cn/tjsj/tjgb_57099/tjgb_57101/202105/t20210508_68020510.html'
	}
	main(file_list)
