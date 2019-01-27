#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import datetime
from transcription import Transcribr
import os

#############################################

app = Flask(__name__)
CORS(app)
db_uri = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)
db.create_all()

#############################################

# TODO: What are we returning?
@app.route("/auth/login", methods=["GET", "POST"])
def login():
    from models import User
    content = request.get_json()
    user = User.query.filter_by(email=content['email']).first()
    if user.check_password(content['password']):
        status = "success"
    else:
        status = "denied"

    return jsonify({"result": "status"})        

@app.route("/auth/register", methods=["GET", "POST"])
def sign_up():
    from models import User
    content = request.get_json()
    try:
        hashed_pw = generate_password_hash(content['password'])
        new_user = User(content['firstName'], content['lastName'],
                        content['email'], hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"result}": "User added"})
    except sqlalchemy.exc.IntegrityError: # user already exists
        return jsonify({"result": "User already exists"})

@app.route("/transcribe", methods=["GET", "POST"])
def fileupload():
    # TODO: determine how fie will be communicated,
    # how to parse json to give file to transcription.py,
    # how user authentication will be verified
    UPLOAD_FOLDER = '/files/translate'
    ALLOWED_EXTENSIONS = set(['mp4', 'wav'])

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
