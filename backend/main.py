#!/usr/bin/python3
import json, os, datetime
from validate_email import validate_email
from flask import Flask, request, Response
from flask_cors import CORS
from flask_jwt import JWT, jwt_required, current_identity
from flask_jwt_extended import JWTManager, create_access_token
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from transcription import Transcribr

app = Flask(__name__)
CORS(app)
db_uri = 'sqlite:////tmp/test.db'

app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Access-Control-Request-Headers'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)
jwt = JWTManager(app)
app.secret_key = os.urandom(24)
app.config['JWT_SECRET_KEY'] = os.urandom(24)

#############################################

def identity(payload):
    user_id = payload['identity']
    return User.query.get(int(user_id))

@app.route("/auth/login", methods=["GET", "POST"])
def login():
    from models import User
    db.create_all()
    content = request.get_json()
    if len(content['password']) < 8:
        return Response(json.dumps({"ERROR": "Password must be at least 8 characters"}), status="401")
    if not validate_email(content['email']):
        return Response(json.dumps({"ERROR": "Email is not valid"}), status="401")
    if content['email'] != "" and content['password'] != "":
        user = User.query.filter_by(email=content['email']).first()
        if user is not None:
            if user.check_password(content['password']):
                id = user.id
                message = "User Authenticated"
                status = "SUCCESS"
                status_code = "200"
                access_token = create_access_token(identity=id)
                resp = json.dumps({status: message, "token": access_token})
            else:
                status = "ERROR"
                message = "Incorrect password"
                status_code = "401"
                resp = json.dumps({status:message})
        else:
            status = "ERROR"
            message = "User does not exist"
            status_code = "401"
            resp = json.dumps({status:message})
    else:
        status = "ERROR"
        status_code = "401"
        message = "Username or password cannot be empty"
        resp = json.dumps({status: message})

    return Response(resp, status=status_code)        

@app.route("/auth/register", methods=["GET", "POST"])
def sign_up():
    from models import User
    db.create_all()
    content = request.get_json()
    try:
        if len(content['password']) < 8:
            return Response(json.dumps({"ERROR":"Password must be at least 8 characters"}), status="401")
        
        if not validate_email(content['email']):
            return Response(json.dumps({"ERROR": "Email is not valid"}), status="401")
            
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
        message = "User already exists"
        status_code = "401"
    return Response(json.dumps({status: message}), status=status_code)

@app.route("/transcribe", methods=["GET", "POST"])
# @jwt_required()
def fileupload():
    from pprint import pprint
    pprint(request.headers)
    pprint(request.data)
    pprint(request.files)
    # TODO: determine how fie will be communicated,
    # how to parse json to give file to transcription.py,
    # how user authentication will be verified
    #UPLOAD_FOLDER = '/translate_files/translate/'
    #ALLOWED_EXTENSIONS = set(['mp4', 'wav'])
    #target = os.path.join(UPLOAD_FOLDER, 'test_docs')
    #print(os.path.exists(target))
    # if not os.path.exists(target):
    #     os.makedirs(target)
    #file = request.files['file']
    #filename = secure_filename(file.filename)
    #destination = "/".join([target, filename])
    #file.save(destination)
    
    #ts = Transcribr(file)
    #session['uploadFilePath'] = destination
    resp = Response(json.dumps({"STATUS": "MESSAGE"}))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

#############################################

jwt = JWT(app, login, identity)
