import datetime
from werkzeug.security import (generate_password_hash,
                               check_password_hash)
from databases.db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, email, password, is_admin=False):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.is_admin = is_admin

    def json(self):
        return {"id": self.id, "name": self.name, "email": self.email, "isAdmin": self.is_admin}

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)
