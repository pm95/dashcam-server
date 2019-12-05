from flask import Flask, request, session, jsonify, make_response, send_file
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


@app.route('/')
def healthcheck():
    return "SecureDashboard server is healthy"


# new routes
@app.route('/api/login', methods=['POST'])
@cross_origin()
def user_login():
    email = (request.data).decode('utf-8')
    conn = sqlite3.connect(CONFIG.DB_PATH)
    c = conn.cursor()
    args = (email,)
    print(email)
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
    return jsonify({
        "firstName": "NOT FOUND",
        "lastName": "NOT FOUND",
        "email": "NOT FOUND",
        "plan": "NOT FOUND",
    })


@app.route('/api/signup', methods=['POST'])
@cross_origin()
def create_user():
    response = ""
    data = request.get_json(force=True)
    print(data)
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
    print(response)
    return response


@app.route('/api/submit', methods=['POST'])
@cross_origin()
def post_video():
    form_data = request.form

    videoName = form_data.get("videoName")
    email = form_data.get("email")

    conn = sqlite3.connect(CONFIG.DB_PATH)
    c = conn.cursor()
    args = (videoName, email,)
    c.execute("SELECT * FROM VIDEOS WHERE videoName=? and email=?", args)
    matches = c.fetchall()
    if matches == []:
        # insert new record into database with user email + video name
        print("inserted new value into database")
        c.execute("INSERT INTO VIDEOS (videoName, email) VALUES (?, ?)", args)
        conn.commit()

        # save video file to disk
        target = os.path.join(UPLOAD_FOLDER, './')
        if not os.path.isdir(target):
            os.mkdir(target)
        vid_file = request.files['file']
        filename = secure_filename(vid_file.filename)
        destination = "/".join([target, filename])
        vid_file.save(destination)
        session['uploadFilePath'] = destination
        response = "success"
    else:
        print("videoName + email combination already exists")
        response = "failure"
    c.close()
    return response


@app.route('/api/updateuser', methods=['POST'])
@cross_origin()
def get_user_data():
    data = request.get_json(force=True)
    print(data)
    try:
        conn = sqlite3.connect(CONFIG.DB_PATH)
        c = conn.cursor()
        args = (
            data["firstName"],
            data["lastName"],
            data["plan"],
            data["email"],
        )
        c.execute(
            "UPDATE USERS SET firstName=?, lastName=?, plan=? WHERE email=?",
            args
        )
        conn.commit()
        c.close()
        return "Updated your information"
    except:
        return "Could not update your information right now"


# routes in progress right now
@app.route('/api/history', methods=['POST'])
@cross_origin()
def get_user_history():
    email = (request.data).decode('utf-8')
    print(email)
    conn = sqlite3.connect(CONFIG.DB_PATH)
    c = conn.cursor()
    args = (
        email,
    )
    c.execute(
        "SELECT videoName FROM VIDEOS WHERE email=?",
        args
    )
    matches = [tup[0] for tup in c.fetchall()]
    c.close()

    if matches != []:
        return jsonify({
            "videos": matches
        })
    return jsonify({
        "videos": []
    })


@app.route('/api/getvideo', methods=['POST'])
@cross_origin()
def get_video():
    vid_name = (request.data).decode('utf-8')
    vid_path = os.path.join(UPLOAD_FOLDER, vid_name)
    return send_file(vid_path)


app.secret_key = os.urandom(24)
app.run(debug=True, host="0.0.0.0")
CORS(app, expose_headers='Authorization')
