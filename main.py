from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
with open('secret.txt', 'r') as myfile:
    app.config['SECRET_KEY']=myfile.read().replace('\n', '')
with open('passkey.txt', 'r') as myfile:
    passkey=myfile.read().replace('\n', '')
socketio = SocketIO(app)
print passkey
@app.route("/")
def main():
	return render_template("index.html")
@app.route("/test/")
def test():
	return render_template("station.html",name="test")
@app.route("/fd/", methods=['POST'])
def fd():
	if request.form['passkey'] != passkey:
		return "fail"
	return render_template("fd.html")
@app.after_request
def no_cache(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'no-cache, no-store'
    response.headers['Pragma'] = 'no-cache'
    return response
if __name__ == '__main__':
	socketio.run(app, "0.0.0.0", 3000)