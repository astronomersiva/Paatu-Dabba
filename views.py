import os
import eyed3
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug import secure_filename

SONGS_UPLOAD_FOLDER = 'static/uploads'
ALBUM_ART_FOLDER = 'static/albumart/'
ALLOWED_EXTENSIONS = set(['mp3'])

app = Flask(__name__)

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_song(filename):
	return send_from_directory(SONGS_UPLOAD_FOLDER, filename)


@app.route('/art/<filename>')
def uploaded_art(filename):
	return send_from_directory(ALBUM_ART_FOLDER, filename)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/podu', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		files = request.files.getlist("file")
		for file in files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				print filename
				file.save(os.path.join(SONGS_UPLOAD_FOLDER, filename))
				#Extract album_art
				try:
					audio_file = eyed3.load('static/uploads/'+filename)
					image_url = 'static/albumart/' + filename.strip('.mp3') + '.jpg'
					with open(image_url, 'wb') as output:
						output.write(audio_file.tag.images[0].image_data)
				except:
					pass
				return render_template('upload.html', prog='1')
		return render_template('upload.html', prog='-1')

	return render_template('upload.html', prog='0')


@app.route('/paadu')
def play():
	songs = []
	for song in os.listdir(SONGS_UPLOAD_FOLDER):
		s = {}
		try:
			audio_file = eyed3.load('static/uploads/'+song)
			if audio_file.tag.title is not None:
				s['title'] =  audio_file.tag.title
			else:
				s['title'] = song.strip('.mp3')
			if audio_file.tag.artist is not None:
				s['artist'] =  audio_file.tag.artist
			if audio_file.tag.album is not None:
				s['album'] =  audio_file.tag.album
			s['url'] = url_for('uploaded_song', filename=song)
			art_name = song.strip('.mp3') + '.jpg'
			if art_name in os.listdir(ALBUM_ART_FOLDER):
				s['art'] = url_for('uploaded_art', filename=art_name)
			else:
				s['art'] = url_for('uploaded_art', filename='placeholder.jpg')
			songs.append(s)
		except:
			pass
	return render_template('play.html', songs=songs)


@app.route('/sudu')
def share():
	songs = []
	for song in os.listdir(SONGS_UPLOAD_FOLDER):
		s = {}
		try:
			audio_file = eyed3.load('static/uploads/'+song)
			if audio_file.tag.title is not None:
				s['title'] =  audio_file.tag.title
			else:
				s['title'] = song.strip('.mp3')
			if audio_file.tag.artist is not None:
				s['artist'] =  audio_file.tag.artist
			if audio_file.tag.album is not None:
				s['album'] =  audio_file.tag.album
			s['url'] = url_for('uploaded_song', filename=song)
			art_name = song.strip('.mp3') + '.jpg'
			if art_name in os.listdir(ALBUM_ART_FOLDER):
				s['art'] = url_for('uploaded_art', filename=art_name)
			songs.append(s)
		except:
			pass
	return render_template('share.html', songs=songs)


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)