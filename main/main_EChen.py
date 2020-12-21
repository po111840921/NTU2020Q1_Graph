import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, request,jsonify,g,session
import json
from werkzeug.utils import secure_filename
from linechart import linechart

UPLOAD_FOLDER = 'C:\\python\\Flask_Current1\\static'
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

@app.route("/bar_home", methods=['GET', 'POST'])
def submit_file_bar():
	if request.method == 'POST':
		file = request.files['file']
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename)) #下載到被指定為UPLOAD_FOLDER的資料夾
		#上傳就進行資料處理
		g.send_file = file.filename
		return render_template("Bar.html",confirm = 1, send_file =file.filename)
		return redirect("/curve_home_go_to_next_page") 
	return render_template("Bar.html",confirm = '', send_file = '')

@app.route("/bar_home_go_to_next_page", methods=['GET', 'POST'])	
def go_to_next_page_bar():
	return redirect("/bar_set") 

@app.route("/bar_set", methods=['GET', 'POST'])
def submit_color_button_bar():
	if request.method == 'POST':
					button = request.form["submit_button"]
					return render_template("Bar.html",confirm = 2) 
					return redirect("/bar_success")
	return render_template("bar.html",confirm = 2,send_file = g.send_file)

@app.route("/bar_success", methods=['GET', 'POST'])
def bar_scuccess():
	if request.method == 'POST':
					image = linechart(UPLOAD_FOLDER+'/'+filename,'green',[1275.84, 335.84 ],['20200101','20201101'],1)
					#input filename, color, x and y range, time range
					# x axis must be time axis
					image.CurveRecognize()
					image.LockCurve()
					image.smooth()
					data = image.output()
					name = filename.split('.')[0]
					data.to_csv(f'/Users/Kyle/Desktop/Flask_Current/static/{name}.csv')
					return render_template("bar.html",confirm = 2) 
					return redirect("/bar1")
	return render_template("bar.html",confirm = 3)

@app.route("/curve_home", methods=['GET', 'POST'])			
def submit_file_curve():				
	if request.method == 'POST':
					file = request.files['file']
					filename = secure_filename(file.filename)
					file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename)) #下載到被指定為UPLOAD_FOLDER的資料夾
					#上傳就進行資料處理
					session['filename_var'] = filename
					return render_template("Curve.html",confirm = 1, send_file =filename)
					#return redirect("/curve_home_go_to_next_page") 
	return render_template("Curve.html",confirm = '', send_file = '')

@app.route("/curve_home_go_to_next_page", methods=['GET', 'POST'])	
def go_to_next_page_curve():
	filename_var = session.get('filename_var', None)
	session['filename_var'] = filename_var
	return redirect("/curve_set") 

@app.route("/curve_set", methods=['GET', 'POST']) #要在curve_set這邊進行圖像辨識
def submit_color_button_curve():
	if request.method == 'POST':
		color = request.form["submit_button"]
		filename_var = session.get('filename_var', None)
		Yrange = [int(i) for i in request.form["Yaxis"].split(',')]
		Xrange = request.form["Xaxis"].split(',')
		image = linechart(UPLOAD_FOLDER+'/'+filename_var,color,Yrange,Xrange,1)
		#input filename, color, x and y range, time range
		# x axis must be time axis
		image.CurveRecognize()
		image.LockCurve()
		image.smooth()
		data = image.output()
		name = filename_var.split('.')[0]
		data.to_csv(f'C:\\Users\\TsaiYiChen\\Flask_Current1\\static\\{name}.csv')
		return render_template("Curve.html",confirm = 3) 
	filename_var = session.get('filename_var', None)
	session['filename_var'] = filename_var
	return render_template("Curve.html", confirm = 2, send_file = filename_var)

@app.route("/curve_home_go_to_next_page1", methods=['GET', 'POST'])	
def go_to_next_page_curve1():
	filename_var = session.get('filename_var', None)
	session['filename_var'] = filename_var
	return redirect("/curve_success") 

@app.route("/curve_success", methods=['GET', 'POST'])
def curve_scuccess():
	if request.method == 'POST':
		filename_var = session.get('filename_var', None)
	return render_template("Curve.html",confirm = 3)


@app.route("/spotcurve_home", methods=['GET', 'POST'])			
def submit_file_spotcurve():				
	if request.method == 'POST':
					file = request.files['file']
					filename = secure_filename(file.filename)
					file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename)) #下載到被指定為UPLOAD_FOLDER的資料夾
					#上傳就進行資料處理
					return render_template("Spotcurve.html",confirm = 1, send_file =file.filename)
					return redirect("/spotcurve_home_go_to_next_page") 
	return render_template("Spotcurve.html",confirm = '', send_file = '')

@app.route("/spotcurve_home_go_to_next_page", methods=['GET', 'POST'])	
def go_to_next_page_spotcurve():
	return redirect("/spotcurve_set") 

@app.route("/spotcurve_set", methods=['GET', 'POST'])
def submit_color_button_spotcurve():
	if request.method == 'POST':
					button = request.form["submit_button"]
					return render_template("Spotcurve.html",confirm = 2) 
					return redirect("/spotcurve_success")
	return render_template("Spotcurve.html",confirm = '')

@app.route("/spotcurve_success", methods=['GET', 'POST'])
def spotcurve_scuccess():
	if request.method == 'POST':
		image = linechart(UPLOAD_FOLDER+'/'+filename,'green',[1275.84, 335.84 ],['20200101','20201101'],1)
		#input filename, color, x and y range, time range
		# x axis must be time axis
		image.CurveRecognize()
		image.LockCurve()
		image.smooth()
		data = image.output()
		name = filename.split('.')[0]
		data.to_csv(f'/Users/Kyle/Desktop/Flask_Current/static/{name}.csv')
		return render_template("Spotcurve.html",confirm = 2) 
	return render_template("Spotcurve.html",confirm = 3)

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
	app.secret_key = 'super secret key'
	app.config['SESSION_TYPE'] = 'filesystem'
	app.debug = True
	app.run(debug = True)