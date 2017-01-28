from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fb_posts_analysis'
socketio = SocketIO(app)

@socketio.on('post')
def getPost(post):
	print post

@socketio.on('user')
def getAllPosts(posts):
	print posts

if __name__ == '__main__':
    socketio.run(app)
