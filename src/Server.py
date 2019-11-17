import os
from flask import Flask, flash, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging


UPLOAD_FOLDER = '../assets/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/healthcheck')
def healthcheck():
    return "Server is Healthy"


@app.route('/api/submit', methods=['POST'])
def post_video():
    target = os.path.join(UPLOAD_FOLDER, './')
    if not os.path.isdir(target):
        os.mkdir(target)
    vid_file = request.files['file']
    filename = secure_filename(vid_file.filename)
    destination = "/".join([target, filename])
    vid_file.save(destination)
    session['uploadFilePath'] = destination
    return jsonify({"res": "Video uploaded successfully"})


app.secret_key = os.urandom(24)
app.run(debug=True, host="0.0.0.0")
CORS(app, expose_headers='Authorization')
