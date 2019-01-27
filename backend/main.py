#!/usr/bin/python3
from flask import Flask, request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import datetime
from transcription import Transcribr
import os
#############################################
app = Flask(__name__)
db_uri = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)
db.create_all()
#############################################
# TODO: What are we returning?
@app.route("/login", methods=["GET", "POST"])
def login():
    from models import User
    content = request.get_json()
    user = User.query.filter_by(email=content['email']).first()
    if user.check_password(content['password']):
        return "User logged in"
    else:
        return "User DENIED"        


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    from models import User
    content = request.get_json()
    print(content)
    hashed_pw = generate_password_hash(content['password'])
    new_user = User(content['firstName'], content['lastName'], 
                    content['email'], hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return "User is signed up!"

@app.route("/auth/register")
def auth_register():
    # need to add import for google_auth class, when it's created
    pass

@app.route("/auth/login")
def auth_login():
    # this will allow login with google auth
    pass

@app.route("/transcribe", methods=["GET", "POST"])
def fileupload():
    # TODO: determine how fie will be communicated,
    # how to parse json to give file to transcription.py,
    # how user authentication will be verified
    UPLOAD_FOLDER = '/path/to/the/uploads'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

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

#############################################
