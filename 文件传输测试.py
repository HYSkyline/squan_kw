from flask import Flask, request, render_template
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'material'  # 指定上传文件夹
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '没有选择文件'
    
    file = request.files['file']
    if file.filename == '':
        return '没有选择文件'
    
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return '文件上传成功'

if __name__ == '__main__':
    app.run(debug=True)
