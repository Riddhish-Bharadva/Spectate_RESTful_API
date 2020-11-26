# Importing required libraries.
from DBConnection import DBConnect
from CreateDatabaseTables import CreateDBStructure
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from UserAndDBDetails import *
import json
from DBOperations import Perform

app = Flask(__name__)
api = Api(app)
app.secret_key = "SecretKey"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://"+username+":"+password+"@"+host+"/"+databaseName
db = SQLAlchemy(app)

# Below class is responsible to create database and tables in case they do not already exist. This will be a case when program runs for first time.
class APIService:
    def API(self):
        ConnectionObject = DBConnect()
        CDB = CreateDBStructure()
        DBStatus = ConnectionObject.Connect("None")
        CDB.CreateDatabase(DBStatus)
        DBStatus = ConnectionObject.Connect("spectateTest")
        CDB.CreateTables(DBStatus)

AS = APIService() # Creating object of class APIService.
AS.API() # Calling method.

class GetEventById(Resource):
    def get(self,id):
        P = Perform() # Creating object of Class Perform written in DBOperations.
        return P.getDataById(id)

class GetSportByStartTime(Resource):
    def get(self): # In this function, in case match name, sport name and order all parameters are passed, priority will be given to match name and data will be returned accordingly.
        Game = request.args.get('sport') # Fetching parameters passed in URL.
        Ordering = request.args.get('ordering') # Fetching parameters passed in URL.
        MatchName = request.args.get('name') # Fetching parameters passed in URL.
        P = Perform() # Creating object of Class Perform written in DBOperations.
        if MatchName != None: # In case matchname is not none, i.e. in case matchname is passed.
            return {"Data by Match":P.getDataByMatchName(MatchName)}
        else: # In case matchname is none, i.e. in case matchname is not passed.
            return {"Data by Sport and Order":P.getDataByGameOrder(Game,Ordering)}

class IntoDB(Resource):
    def RunThis(self, data):
        P = Perform() # Creating object of class Perform.
        if data != None and data != {}: # This condition will handle if data passed in JSON is blank or not.
            if data.get("message_type").lower() == "newevent":
                if P.AddData(data) == "Success":
                    return {"message":"NewEvent added successfully."}
                elif P.AddData(data) == "Duplicate Entry":
                    return {"message":"Duplicate record. This message id or event id already exists in database."}
                else:
                    return {"message":"Error occurred while adding NewEvent. Please try again."}
            elif data.get("message_type").lower() == "updateodds":
                if P.UpdateData(data) == "Success":
                    return {"message":"Data updated successfully."}
                else:
                    return {"message":"Error occurred while updating data. Please try again."}
            else:
                return {"message":"Un-identified message_type. Please try again with correct messege_type."}
        else: # In case no json data is passed, simply return message accordingly.
            return {"message":"No json data passed."}

    def post(self):
        data = request.get_json() # Accepting json data and storing in form of data dictionary.
        return self.RunThis(data)

    def put(self):
        data = request.get_json() # Accepting json data and storing in form of data dictionary.
        return self.RunThis(data)

api.add_resource(GetEventById, '/api/match/<id>') # This API will accept Event id as parameter from URL.
api.add_resource(GetSportByStartTime, '/api/match/') # This API will accept sport name and order parameters from URL.
api.add_resource(IntoDB, '/api/createOrUpdate') # This API will be used to handle addition and updation of data in db. GET will not be allowed. Only methods POST and PUT are allowed using this API and hence mentioned.

if __name__ == "__main__":
    app.run(debug=False)
