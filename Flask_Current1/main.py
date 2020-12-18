import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, request,jsonify
import json
from werkzeug.utils import secure_filename
from linechart import linechart

UPLOAD_FOLDER = '/Users/Kyle/Desktop/Flask_Current1/static'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

def allowed_file(filename): #篩選合格的file格式
    return '.' in filename and\
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#函數結構：一對一 或 多對一
@app.route("/", methods=['GET', 'POST'])
def home():
	return render_template("home.html")

confirm = 0
@app.route("/bar", methods=['GET', 'POST'])
def bar():
	#if request.method == 'GET':

	if request.method == 'POST':
	   file = request.files['file']
	   if file and allowed_file(file.filename):
	      filename = secure_filename(file.filename)
	      file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename)) #下載到被指定為UPLOAD_FOLDER的資料夾
	      #上傳就進行資料處理
	      image = linechart(UPLOAD_FOLDER+'/'+filename,'green',[1275.84, 335.84 ],['20200101','20201101'],1)
	      #input filename, color, x and y range, time range
	      # x axis must be time axis
	      image.CurveRecognize()
	      image.LockCurve()
	      image.smooth()
	      data = image.output()
	      name = filename.split('.')[0]
	      data.to_csv(f'/Users/Kyle/Desktop/Flask_Current/static/{name}.csv')
	      return render_template("Bar.html",confirm = 1, send_file =file.filename) 

	if request.method == 'GET':
	   button = request.form['submit_button']
	   if button == 'Do Something':
	      return "abc"


	return render_template("Bar.html",confirm = '', send_file = '')


@app.route("/curve", methods=['GET', 'POST'])
def curve():
	return render_template("Curve.html")
	def upload_file():
	    if request.method == 'POST':
	       file = request.files['file']
	       if file and allowed_file(file.filename):
	          filename = secure_filename(file.filename)
	          file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename)) #下載到被指定為UPLOAD_FOLDER的資料夾
	          filenamelist.append(filename)




@app.route("/spotcurve", methods=['GET', 'POST'])
def spotcurve():
	return render_template("Spotcurve.html")
	def upload_file():
	    if request.method == 'POST':
	       file = request.files['file']
	       if file and allowed_file(file.filename):
	          filename = secure_filename(file.filename)
	          file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename)) #下載到被指定為UPLOAD_FOLDER的資料夾
	          return render_template("index.html", user_image = full_filename)
	          """return redirect(url_for('uploaded_file',filename = filename)) #當檔案上傳完，會跳轉到 uploaded_file() 函式，並帶著參數 filename"""



@app.route("/foundingteam", methods=['GET', 'POST'])
def foundingteam():
	return render_template("Founding Team.html")

@app.route("/learnmore", methods=['GET', 'POST'])
def learnmore():
	return render_template("Learnmore.html")


"""@app.route('/uploads/curve/<filename>') #從local回傳檔案回http://127.0.0.1:5000/uploads/<filename>
def uploaded_file_curve(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)  """

if __name__ == "__main__":
	app.run(debug = True)

