# All the classes in this .py files are used for object relational mapping. Each class represents mapping with database table.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from UserAndDBDetails import *
from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://"+username+":"+password+"@"+host+"/"+databaseName
db = SQLAlchemy(app)

class messagedetails(db.Model):
    __tablename__ = "messagedetails"
    id = db.Column(db.BigInteger, primary_key=True)
    message_type = db.Column(db.String(25))
    Evid = db.Column(db.BigInteger)

    def __init__(self,id,message_type,Evid):
        self.id = id
        self.message_type = message_type
        self.Evid = Evid

class eventdetails(db.Model):
    __tablename__ = "eventdetails"
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(25))
    startTime = db.Column(db.DateTime)
    sportId = db.Column(db.Integer)

    def __init__(self,id,name,startTime,sportId):
        self.id = id
        self.name = name
        self.startTime = startTime
        self.sportId = sportId

class sportsdetails(db.Model):
    __tablename__ = "sportsdetails"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))

    def __init__(self,id,name):
        self.id = id
        self.name = name

class evtomark(db.Model):
    __tablename__="evtomark"
    Evid = db.Column(db.BigInteger, primary_key=True)
    Mid = db.Column(db.BigInteger, primary_key=True)

    def __init__(self,Evid,Mid):
        self.Evid = Evid
        self.Mid = Mid

class marketdetails(db.Model):
    __tablename__ = "marketdetails"
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(25))

    def __init__(self,id,name):
        self.id = id
        self.name = name

class marktosel(db.Model):
    __tablename__="marktosel"
    Mid = db.Column(db.BigInteger, primary_key=True)
    Sid = db.Column(db.BigInteger, primary_key=True)

    def __init__(self,Mid,Sid):
        self.Mid = Mid
        self.Sid = Sid

class selectionsdetails(db.Model):
    __tablename__ = "selectionsdetails"
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(25))
    odds = db.Column(db.Float)

    def __init__(self,id,name,odds):
        self.id = id
        self.name = name
        self.odds = odds
