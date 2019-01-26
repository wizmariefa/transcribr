from flask import Flask, request, redirect
from werkzeug.utils import secure_filename
from google_auth import Google_Auth
from transcription import Transcribr
from flask_sqlalchemy import SQLAlchemy
import os
#############################################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(12), nullable = False)
    lastName = db.Column(db.String(12), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwordHash = db.Column(db.String(256), nullable = False)
    registeredOn = db.Column(db.String(120), nullable=False)
    gcpAuthToken = db.Column(db.String(120))
    gcpRefreshToken = db.Column(db.String(120))

    def __init__(self, firstName, lastName, email, passwordHash, gcpAuthToken=None, gcpRefreshToken = None):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.passwordHash = passwordHash
        self.gcpAuthToken = gcpAuthToken
        self.gcpRefreshToken = gcpRefreshToken
        self.registered_on = datetime.utcnow()


#############################################

@app.route("/login")
def login():
    # login user with password
    pass

@app.route("/signup")
def sign_up():
    # sign up new user
    pass

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
    # this will be called to upload and transcribe file
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

if __name__ == "__main__":
    app.run()
