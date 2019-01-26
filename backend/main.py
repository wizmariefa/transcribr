from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(12), nullable = False)
    lastName = db.Column(db.String(12), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwordHash = db.Column(db.String(256), nullable = False)
    gcpAuthToken = db.Column(db.String(120))
    gcpRefreshToken = db.Column(db.String(120))

    def __repr__(self):
        return '<User %r>' % self.email

@app.route("/")
def main():
    pass

@app.route("/auth/register")
def auth_register():
    # need to add import for google_auth class, when it's created
    pass

@app.route("/auth/login")
def auth_login():
    pass

if __name__ == "__main__":
    app.run()