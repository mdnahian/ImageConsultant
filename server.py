from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import json
import os.path
from imageconsultant import imageconsultant

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'fb_posts_analysis'
socketio = SocketIO(app)

static_folder = 'static/'
sample = 'hackathon.json'

@app.route('/')
def init():
        return render_template('index.html')

@socketio.on('post')
def getPost(post):
	sentence, j = imageconsultant(post)
	#print post
	#print sentence
	#print json
	
	stone = []	

	sentence_data = json.loads(sentence)
	sentence_tones = ''	
	
	if 'sentences_tone' not in sentence_data:
		pass	
	else:
		sentence_tones = sentence_data['sentences_tone']
		for sentence_tone in sentence_tones:
			tone_categories = sentence_tone['tone_categories']
			s = []
			s.append(sentence_tone['text'])
			for tone_category in tone_categories:
				tones = tone_category['tones']
				score = 0
				winner = ''
				for tone in tones:
					current = float(tone['score'])
					if current > score:
						winner = tone['tone_name']
						score = float(tone['score'])
						print score
						print winner
				s.append(winner)
			stone.append(s)	
	
		print stone
		html = ''
		for m in stone:
			underline = ''
			style = ''
			bg = ''
			for s in m:
				if len(s) < 20:
					s = s.strip()
					print s
					if s == 'Anger':
						underline = 'red'
					elif s == 'Disgust':
						underline = 'green'
					elif s == 'Fear':
						underline = 'purple'
					elif s == 'Joy':
						underline = 'yellow'
					elif s == 'Sadness':
						underline = 'blue'
					
					if s == 'Analytical':
						style = '"Times New Roman", Times, serif'
					elif s == 'Confident':
						style = 'Arial, Helvetica, sans-serif'
					elif s == 'Tentative':
						style = '"Comic Sans MS", cursive, sans-serif'

					if s == 'Openness':
						bg = 'pink'
					elif s == 'Conscientiousness':
						bg = 'green'
					elif s == 'Extraversion':
						bg = 'yellow'
					elif s == 'Agreeableness':
						bg = 'blue'
					elif s == 'Emotional Range':
						bg = 'orange'
					
				
			html += '<span style=\'border:3px solid '+underline+'; font-style:'+style+'; background-color:'+bg+'; \'><span style="color:#000;">'+m[0]+"</span></span>"		
		print html
		emit('responseData', html)

@socketio.on('posts')
def getAllPosts(posts):
	posts_data = json.loads(posts)
	f = open(static_folder+sample,'w')
	f.write(posts)
	f.close()
	#emit('postsSuccess', posts)

@socketio.on('contentLoaded')
def isContentLoaded(data):
	if(os.path.isfile(static_folder+sample)):
		emit('isUserLoaded', 'true') 

@app.route('/<path:path>')
def sound_file(path):
	return url_for('static', filename=path)

if __name__ == '__main__':
    #context = ('static/hello.crt', 'static/hello.key')
    socketio.run(app, host='0.0.0.0', port=int(80))
