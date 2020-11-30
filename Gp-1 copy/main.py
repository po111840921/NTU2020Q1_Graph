from flask import Flask, render_template

app = Flask(__name__)

@app.route("/home")
@app.route("/")
def home():
	return render_template("/Users/Kyle/Desktop/Insurance Class/Gp-1/Flask/templates/home.html")

if __name__ == '__main__':
    app.run(debug = True)  