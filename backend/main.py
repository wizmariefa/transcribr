from flask import Flask, request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from google_auth import Google_Auth
from transcription import Transcribr
import os
#############################################
app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
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

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


#############################################
# TODO: What are we returning?
@app.route("/login", methods=["GET", "POST"])
def login(user_info):
    content = request.get_json()
    user = User.query.filter_by(email=content['email']).first()
    return generate_password_hash(content['password']) == user.passwordHash

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    content = request.get_json()
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
@login_required
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
