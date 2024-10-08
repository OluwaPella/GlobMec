from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(60), nullable=False)
    contact = db.Column(db.Integer, unique=True, nullable=False)
    services = db.Column(db.String(), nullable=False)
    addresses = db.relationship('Address', back_populates='user')
    bookings = db.relationship('Booking', back_populates='user')
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at =  db.Column(db.DateTime, onupdate=datetime.now())

    
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String) 
    state = db.Column(db.String)
    city =  db.Column(db.String)
    districts = db.Column(db.String)
    provinces = db.Column(db.String)
    street = db.Column(db.String)
    zipcode = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    user = db.relationship('User', back_populates='addresses')

class Session(db.model):
    Session_id = db.Column(db.string, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    user = db.relationship('User', back_populates='sessions')
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at =  db.Column(db.DateTime, onupdate=datetime.now())


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    services = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='bookings')

