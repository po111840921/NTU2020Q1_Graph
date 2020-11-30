#https://medium.com/@charming_rust_oyster_221/flask-%E6%AA%94%E6%A1%88%E4%B8%8A%E5%82%B3%E5%88%B0%E4%BC%BA%E6%9C%8D%E5%99%A8%E7%9A%84%E6%96%B9%E6%B3%95-1-c11097c23137

import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/Users/Kyle/Desktop/Insurance Class/Upload Folder'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

def allowed_file(filename): #篩選合格的file格式
    return '.' in filename and\
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST']) #用來建立上傳的API
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 
                                   filename))
            return redirect(url_for('uploaded_file',filename=filename)) #當檔案上傳完，會跳轉到 uploaded_file() 函式，並帶著參數 filename
    return '''
    <!doctype html>
    <head><head>
    <body>
    <center><title>Bar Chart analysis</title></center>
    <center><h1>Upload new File</h1></center>
    <form action="" method=post enctype=multipart/form-data>
      <center><p><input type=file name=file>
         <input type=submit value=Upload>
    <body>
    </form>
    '''
@app.route('/uploads/<filename>') #從local回傳檔案回http://127.0.0.1:5000/uploads/<filename>
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)    #這邊的filename是我們前面先requests的檔名，用來做index找要會傳回網站的是哪個

if __name__ == '__main__':
    app.run(debug = True)   