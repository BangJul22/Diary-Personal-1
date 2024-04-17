import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get("title_give")
    content_receive = request.form.get("content_give")

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    
    file = request.files.get('file_give')
    profile = request.files.get('profile_give')

    if file and profile:
        extension = file.filename.split('.')[-1]
        filename = f'static/post-{mytime}.{extension}'
        file.save(filename)

        extension = profile.filename.split('.')[-1]
        profilename = f'static/profile-{mytime}.{extension}'
        profile.save(profilename)

        time = today.strftime('%Y.%m.%d')

        doc = {
            'file': filename,
            'profile': profilename,
            'title': title_receive,
            'content': content_receive,
            'time': time,

        }
        db.diary.insert_one(doc)
        return jsonify({'msg': 'Berhasil'})
    else:
        return jsonify({'msg': 'Gagal menyimpan. Pastikan Anda mengunggah file yang sesuai.'}), 400

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
