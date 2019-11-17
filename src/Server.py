import os
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging


UPLOAD_FOLDER = '../assets/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/healthcheck')
def healthcheck():
    return "Server is Healthy"


@app.route('/api/submit', methods=['POST'])
def post_video():
    target = os.path.join(UPLOAD_FOLDER, 'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file']
    filename = secure_filename(file.filename)
    destination = "/".join([target, filename])
    file.save(destination)
    session['uploadFilePath'] = destination
    response = "Whatever you wish too return"
    return response


app.secret_key = os.urandom(24)
app.run(debug=True, host="0.0.0.0")
CORS(app, expose_headers='Authorization')
