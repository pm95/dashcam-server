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


# new routes
@app.route('/api/login', methods=['GET'])
@cross_origin()
def user_login():
    data = request.get_json()
    conn = sqlite3.connect(CONFIG.DB_PATH)
    c = conn.cursor()
    args = (data["email"],)
    c.execute("SELECT * FROM USERS WHERE email=?", args)
    match = c.fetchone()
    print(match)
    if match:
        return jsonify({
            "firstName": match[0],
            "lastName": match[1],
            "email": match[2],
            "plan": match[3],
        })
    return jsonify("user not found")


@app.route('/api/signup', methods=['POST'])
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
        response = "user created"
    else:
        response = "user exists"
    c.close()
    return response


# routes in progress
@app.route('/api/submit', methods=['POST'])
@cross_origin()
def post_video():
    # target = os.path.join(UPLOAD_FOLDER, './')
    # if not os.path.isdir(target):
    #     os.mkdir(target)
    # vid_file = request.files['file']
    # filename = secure_filename(vid_file.filename)
    # destination = "/".join([target, filename])
    # vid_file.save(destination)
    # session['uploadFilePath'] = destination
    # return "Video uploaded successfully"

    # old routes


@app.route('/api/updateuser', methods=['POST'])
@cross_origin()
def get_user_data():
    data = request.get_json()
    conn = sqlite3.connect(CONFIG.DB_PATH)
    c = conn.cursor()
    args = (data["email"],)
    c.execute("SELECT * FROM USERS WHERE email=?", args)
    match = c.fetchone()
    print(match)
    return "updateuser end hit"


app.secret_key = os.urandom(24)
app.run(debug=True, host="0.0.0.0")
CORS(app, expose_headers='Authorization')
