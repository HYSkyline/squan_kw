# -*- coding:utf-8 -*-

from markitdown import MarkItDown
import time
import os


def main(file_list):
	print('Link Start!')
	print('--' * 6)
	time_ori = time.time()

	md_word = file_trans(file_list['word'])
	md_pdf = file_trans(file_list['pdf'])
	md_html = file_trans(file_list['html'])

	print('Word transform result:\n' + md_word + '\n' + '--' * 6)
	print('PDF transform result:\n' + md_pdf + '\n' + '--' * 6)
	print('html transform result:\n' + md_html + '\n' + '--' * 6)

	print('Time escape:' + str(int((time.time() - time_ori) * 100) / 100))
	print('Link Logout.')


if __name__ == '__main__':
	file_list = {
		'word': '',
		'pdf': '',
		'html': ''
	}
	main(file_list)
