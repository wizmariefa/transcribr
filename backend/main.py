#!/usr/bin/python3
import json
from flask import Flask, request, Response
from flask_cors import CORS
from flask_jwt import JWT, jwt_required, current_identity
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import datetime
from transcription import Transcribr
import os

app = Flask(__name__)
CORS(app)
db_uri = 'sqlite:////tmp/test.db'
app.config['JWT_TOKEN_LOCATION'] = ['json']
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
jwt = JWTManager(app)
app.secret_key = os.urandom(24)
app.config['JWT_SECRET_KEY'] = os.urandom(24)


#############################################

def identity(payload):
    user_id = payload['identity']
    return User.query.get(int(user_id))

# TODO: What are we returning?


@app.route("/auth/login", methods=["GET", "POST"])
def login():
    from models import User
    db.create_all()
    content = request.get_json()
    user = User.query.filter_by(email=content['email']).first()
    id = user.id
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
    
    access_token = create_access_token(identity=id)
    resp = json.dumps({status: message, "token": access_token})
    print(resp)
    return Response(resp, status=status_code)        

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
    except IntegrityError:  # user already exists
        status = "ERROR"
        message = "User Denied"
        status_code = "401"
    return Response(json.dumps({status: message}), status=status_code)

@app.route("/transcribe", methods=["GET", "POST"])
@jwt_required
def fileupload():
    # TODO: determine how fie will be communicated,
    # how to parse json to give file to transcription.py,
    # how user authentication will be verified
    # UPLOAD_FOLDER = '/files/translate'
    # ALLOWED_EXTENSIONS = set(['mp4', 'wav'])
    # target = os.path.join(UPLOAD_FOLDER, 'test_docs')
    # if not os.path.isdir(target):
    #     os.mkdir(target)
    print(request.files)
    # file = request.files['file']
    # filename = secure_filename(file.filename)
    # destination = "/".join([target, filename])
    # file.save(destination)
    
    # ts = Transcribr(file)
    # session['uploadFilePath'] = destination
    # response = "Whatever you wish too return"
    return response

#############################################

jwt = JWT(app, login, identity)
