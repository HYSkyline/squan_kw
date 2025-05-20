from flask import Flask, render_template, send_file
from flask import request, url_for, redirect, flash
import time
import os
import requests
from openai import OpenAI
from file_format_trans import file_format_transform
import json
import xlwt
# from werkzeug.utils import secure_filename


global time_origin, file_target
file_target = {
	'file_address': '',
	'proj_name': '',
	'model': '',
	'status': []
}
app = Flask(__name__)

UPLOAD_FOLDER = 'material'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
	os.makedirs(UPLOAD_FOLDER)


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		file_target = {
			'file_address': '',
			'proj_name': '',
			'model': '',
			'status': []
		}
		return render_template('index.html', tarfile=file_target)


@app.route('/upload', methods=['POST'])
def upload_file():
	file = request.files['filepathFILE']
	url_path = request.form.get('filepathURL')
	if file:
		filename = file.filename
		file_target['file_address'] = filename
		# filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	elif url_path != '':
		file_target['file_address'] = url_path
	else:
		return u'输入的文件名和网址均为空白字符串', 400

	file_target['proj_name'] = request.form.get('projName')

	if request.form.get('modeText') == u'本地模式':
		file_target['model'] = 'local'
	else:
		file_target['model'] = 'online'
	return redirect(url_for('progress', tarfile=file_target))


@app.route('/progress', methods=['GET'])
def progress():
	file_target['status'] = []
	time_origin = time.time()
	file_status_log('Start.')
	file_status_log('--' * 6)
	# time_origin存储程序启动时间，用以计算程序各阶段耗时和整体运行时间
	file_status_log(u'当前时间：' + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

	f_path = os.path.join(app.config['UPLOAD_FOLDER'], file_target['file_address'])
	proj_name = file_target['proj_name']
	model = file_target['model']
	# 使用file_format_trans.py中的若干文件预处理函数，对输入的文件进行预处理
	md_content = file_format_transform(f_path, 'temp/md_res_md01.txt')
	# 大模型不能很好完成大文本量的指标抽取，所以按2000字节进行了分段，能有效提高指标抽取的完整性
	md_content_clip_list = content_clip(md_content)

	for i in range(len(md_content_clip_list)):
		# 用time_para来对每一个分段的数据抽取耗时进行统计
		time_para = time.time()
		file_status_log(u'文字信息正在分段提交给大模型解析. 当前进度:(' + str(i + 1) + '/' + str(len(md_content_clip_list)) + ').')
		if model == 'online':
			data_res = data_extract_aliyun(md_content_clip_list[i])	# 输入markdown格式的已经过预处理的内容，返回json的指标抽取结果
			output_check = data_output_aliyun(proj_name, str(i + 1), data_res)	# 指标抽取结果先保存到本地txt，作为缓存文件
		else:
			data_res = data_extract_ollama(md_content_clip_list[i])
			output_check = data_output_ollama(proj_name, str(i + 1), data_res)
		file_status_log(u'本段数据已提取。共耗时:' + str(int((time.time() - time_para) * 100) / 100) + 's.')
		file_status_log('--' * 6)

	# 将数据抽取的过程文本合并，并转化为一整张EXCEL表格
	data_sum(proj_name, model, num_clips=len(md_content_clip_list))
	file_status_log(u'总计耗时:' + str(int((time.time() - time_origin) * 100) / 100) + 's.\n程序已完成.')
	cache_clean()
	return render_template('progress.html', tarfile=file_target)


@app.route('/download', methods=['GET'])
def download():
	return send_file('data\\' + file_target['proj_name'] + '-数据抽取结果.xls', as_attachment=True)


def data_sum(proj_name, model, num_clips):
	file_status_log(u'缓存数据拼合最终表格中……')
	res_sum = []	# 基本形式就如同{"indicator": "全部财税收入（亿元）", "value": 156.40}
	if model == 'online':
		for i in range(num_clips):
			with open('data/' + proj_name + '-' + str(i + 1) + '_aliyun.txt', 'r', encoding='utf-8') as f_cont:
				cont = f_cont.read().replace('\n', '')
			res_json = json.loads(cont)
			# 有时候公报内容长度正好是分段标准的N倍，会出现最后一段是空白，大模型分析后返回的值也是空白
			try:
				for each in res_json['data']:
					res_sum.append(each)
			except Exception as e:
				pass
	else:
		for i in range(num_clips):
			with open('data/' + proj_name + '-' + str(i + 1) + '_ollama.txt', 'r', encoding='utf-8') as f_cont:
				cont = f_cont.read().replace('\n', '')
			res_json = json.loads(cont)
			# 有时候公报内容长度正好是分段标准的N倍，会出现最后一段是空白，大模型分析后返回的值也是空白
			if res_json:
				for each in res_json['data']:
					res_sum.append(each)

	# 创建Excel工作簿和工作表
	workbook = xlwt.Workbook(encoding='utf-8')
	worksheet = workbook.add_sheet(u'数据抽取-指标表')

	# 写入列名（首行）
	worksheet.write(0, 0, u'序号')
	worksheet.write(0, 1, u'指标名称')
	worksheet.write(0, 2, u'指标数值')

	# 写入数据行
	for i in range(len(res_sum)):
		worksheet.write(i + 1, 0, i + 1)
		worksheet.write(i + 1, 1, res_sum[i]['indicator'])
		worksheet.write(i + 1, 2, res_sum[i]['value'])

	# 保存Excel文件
	workbook.save('data/' + proj_name + u'-数据抽取结果.xls')
	file_status_log(u'最终结果已生成为' + proj_name + u'-数据抽取结果.xls，点击下方按钮下载')
	file_status_log('--' * 6)


def cache_clean():
	# 清理temp文件夹下对输入文件进行预处理的过程文件
	cache_file_list = os.listdir('temp/pdf_pages')
	for each in cache_file_list:
		os.remove('temp/pdf_pages/' + each)
	cache_file_list = os.listdir('temp')
	# for each in cache_file_list:
	# 	os.remove('temp/' + each)
	# 清理data文件夹下大模型对每个分段的直接输出结果，仅保留最终拼合的EXCEL指标表
	# cache_file_list = os.listdir('data')
	# for each in cache_file_list:
	# 	if each.split('.')[-1] == 'txt':
	# 		os.remove('data/' + each)
	file_status_log(u'缓存文件已清理完成')
	file_target = {
		'file_address': '',
		'proj_name': '',
		'model': ''
	}


def data_extract_ollama(txt_content):
	# 以local_ollama_ip.config文件存储院里ollama服务器的IP地址
	with open('local_ollama_ip.config', 'r') as f_ip:
		ollama_ips = f_ip.readlines()
	# 以prompt_pre.txt文件存储定制化的提示词前缀
	with open('prompt_pre.txt', 'r', encoding='utf-8') as f_prompt:
		prompt_pre = f_prompt.read()
	url = "http://" + ollama_ips[1][:-1] + ":11434/api/generate"  # 实际使用时，IP 替换为 Ollama 所在的服务器 IP
	payload = {
		"model": "qwq:32b",	# 还可以换成deepseek-r1:32b
		"prompt": prompt_pre + txt_content.replace('\n', '').replace(' ', ''),
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
			return response.text
		else:
			file_status_log(f"大模型处理失败，状态码：{response.status_code}，程序即将退出.")
			exit()
	except Exception as e:
		file_status_log(str(e))
		exit()


def data_extract_aliyun(txt_content):
	with open('prompt_pre.txt', 'r', encoding='utf-8') as f_prompt:
		prompt_pre = f_prompt.read()
	# 以config.config存储api_key的值
	with open('config.config', 'r') as f_key:
		api_key = f_key.readlines()[1].split(':')[1][:-1]
	client = OpenAI(
		api_key=api_key,  # 如何获取API Key：https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
		base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
	)
	completion = client.chat.completions.create(
		model="qwen-plus",	# 还可以换成qwen-max、deepseek-r1等，但使用deepseek时可能返回值的格式不一致，会导致报错
		response_format={"type": "json_object"},
		extra_body={"enable_search": False},
		messages=[
			{'role': 'system', 'content': u'你是一个严格按照提示词要求进行工作的数据助手，你的工作认真而精准，不会遗漏资料中任何细节。'},
			{'role': 'user', 'content': prompt_pre + txt_content.replace('\n', '').replace(' ', '')}
		]
	)
	return completion.choices[0].message.content


def data_output_ollama(proj_name, para_name, res):
	res_json = json.loads(res)['response'].replace('\n', '').replace(' ', '')
	with open(u'data/' + proj_name + '-' + para_name + '_ollama.txt', 'w', encoding='utf-8') as f_res:
		f_res.write(res_json)
	return 200


def data_output_aliyun(proj_name, para_name, res):
	with open(u'data/' + proj_name + '-' + para_name + '_aliyun.txt', 'w', encoding='utf-8') as f_res:
		f_res.write(res)
	return 200


def content_clip(cont):
	max_content_length = 1000
	cont_list = cont.split('\n\n')
	
	res_list = []
	clip_cont = ''
	for i in range(len(cont_list)):
		clip_cont = clip_cont + cont_list[i]
		if len(clip_cont) > max_content_length:
			res_list.append(clip_cont)
			clip_cont = ''
	res_list.append(clip_cont)
	file_status_log(u'已按照' + str(max_content_length) + u'字节长度的标准，将输入内容划分为' + str(len(res_list)) + u'个部分，并将逐个进行数据抽取')
	file_status_log('--' * 6)
	return res_list


def file_status_log(text_content):
	file_target['status'].append(text_content)


if __name__ == '__main__':
	app.run(debug=True)
