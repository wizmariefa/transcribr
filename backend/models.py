#!/usr/bin/python3
from main import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(12), nullable=False)
    lastName = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwordHash = db.Column(db.String(256), nullable=False)
    registeredOn = db.Column(db.String(120), nullable=False)
    gcpAuthToken = db.Column(db.String(120))
    gcpRefreshToken = db.Column(db.String(120))

    def __init__(self, firstName, lastName, email, passwordHash, gcpAuthToken=None, gcpRefreshToken=None):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.passwordHash = passwordHash
        self.gcpAuthToken = gcpAuthToken
        self.gcpRefreshToken = gcpRefreshToken
        self.registeredOn = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def set_password(self, password):
        self.passwordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)
