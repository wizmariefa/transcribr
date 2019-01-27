#!/usr/bin/python3
import json
from flask import Flask, request, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
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

#############################################

# TODO: What are we returning?
@app.route("/auth/login", methods=["GET", "POST"])
def login():
    from models import User
    db.create_all()
    content = request.get_json()
    user = User.query.filter_by(email=content['email']).first()
    if user is not None:
        if user.check_password(content['password']):
            message = "User Authenticated"
            status = "SUCCESS"
            status_code = "200"
        else:
            status = "ERROR"
            message = "User Denied"
            status_code = "401"
    else:
        status = "ERROR"
        message = "User Denied"
        status_code = "401"

    return Response(json.dumps({status: message}), status=status_code)        

@app.route("/auth/register", methods=["GET", "POST"])
def sign_up():
    from models import User
    db.create_all()
    content = request.get_json()
    try:
        hashed_pw = generate_password_hash(content['password'])
        new_user = User(content['firstName'], content['lastName'],
                        content['email'], hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        message = "User Authenticated"
        status = "SUCCESS"
        status_code = "200"
    except IntegrityError: # user already exists
        status = "ERROR"
        message = "User Denied"
        status_code = "401"
    return Response(json.dumps({status: message}), status=status_code)

@app.route("/transcribe", methods=["GET", "POST"])
def fileupload():
    # TODO: determine how fie will be communicated,
    # how to parse json to give file to transcription.py,
    # how user authentication will be verified
    UPLOAD_FOLDER = './files/translate'
    ALLOWED_EXTENSIONS = set(['mp4', 'wav'])

    target = os.path.join(UPLOAD_FOLDER, 'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file']
    filename = secure_filename(file.filename)
    destination = "/".join([target, filename])
    file.save(destination)
    message = "Files Uploaded"
    status_code = "200"
    return Response(json.dumps({'message': message, 'status': 'Success'}), status=status_code)
