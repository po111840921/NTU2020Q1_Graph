import flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('', methods=['GET'])
def index():
    return "<h1>Hello Flaskasd!</h1>"

app.run()