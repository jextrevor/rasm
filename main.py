import eventlet
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
with open('secret.txt', 'r') as myfile:
    app.config['SECRET_KEY']=myfile.read()
socketio = SocketIO(app)

if __name__ == '__main__':
	socketio.run(app, "0.0.0.0", 3000)