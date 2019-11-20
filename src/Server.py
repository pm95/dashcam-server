from flask import Flask, request, session, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin

import os
import time

import sqlite3

import CONFIG

from pprint import pprint


UPLOAD_FOLDER = '../assets/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/healthcheck')
def healthcheck():
    return "Server is Healthy"


@app.route('/api/createuser', methods=['POST'])
@cross_origin()
def create_user():
    response = ""
    data = request.get_json()
    conn = sqlite3.connect(CONFIG.DB_PATH)
    c = conn.cursor()
    args = (data["email"],)
    c.execute("SELECT * FROM USERS WHERE email=?", args)
    match = c.fetchone()

    if not match:
        email = data["email"]
        firstName = data["firstName"]
        lastName = data["lastName"]
        plan = data["plan"]
        args = (firstName, lastName, email, plan,)
        c.execute(
            "INSERT INTO USERS (firstName, lastName, email, plan) VALUES (?, ?, ?, ?)", args)
        conn.commit()
        c.close()
        return "user created"
    c.close()
    return "user exists"


@app.route('/api/fetchuser', methods=['GET', 'POST'])
@cross_origin()
def get_user_data():
    user_data = {
        "firstName": "ServerFirstName",
        "lastName": "ServerLastName",
        "email": "user@serverDomain.com",
        "carMake": "ToyotaServer",
        "carModel": "4RunnerServer",
        "plan": "Free",
        "capacity": "100 GB",
        "available": "100 GB"
    }
    return jsonify(user_data)


@app.route('/api/submit', methods=['POST'])
@cross_origin()
def post_video():
    target = os.path.join(UPLOAD_FOLDER, './')
    if not os.path.isdir(target):
        os.mkdir(target)
    vid_file = request.files['file']
    print(request)
    filename = secure_filename(vid_file.filename)
    destination = "/".join([target, filename])
    vid_file.save(destination)
    session['uploadFilePath'] = destination
    return "Video uploaded successfully"


app.secret_key = os.urandom(24)
app.run(debug=True, host="0.0.0.0")
CORS(app, expose_headers='Authorization')
