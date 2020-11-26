from TableClass import *
from UserAndDBDetails import *
from datetime import datetime
from sqlalchemy import update, desc

app = Flask(__name__)
app.secret_key = "SecretKey"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://"+username+":"+password+"@"+host+"/"+databaseName
db = SQLAlchemy(app)

# Below class and functions are collectively responsible to perform all operations on DB.
class Perform:
    def getDataById(self, id): # This method is responsible to fetch data from DB using event id passed in URL of our defined API.
        Data = {}
        marketData = []
        evvalue = eventdetails.query.filter_by(id = id).first()
        if evvalue != None: # This condition handles case when no event id is passed in URL.
            sportvalue = sportsdetails.query.filter_by(id = evvalue.sportId).first()
            Data["id"] = evvalue.id
            Data["url"] = "http://localhost:5000/api/match/"+str(evvalue.id)
            Data["name"] = evvalue.name
            Data["startTime"] = evvalue.startTime.strftime("%Y-%m-%d %H:%M:%S")
            Data["sport"] = {"id":sportvalue.id,"name":sportvalue.name}
            marketIds = evtomark.query.filter(evtomark.Evid == evvalue.id).all()
            for eachId in marketIds:
                marketvalue = marketdetails.query.filter_by(id = eachId.Mid).first()
                value = {}
                value["id"]=marketvalue.id
                value["name"]=marketvalue.name
                selectionsData = []
                selectionsIds = marktosel.query.filter(marktosel.Mid == marketvalue.id).all()
                for eachSelId in selectionsIds:
                    selectionvalue = selectionsdetails.query.filter_by(id = eachSelId.Sid).first()
                    selvalue = {}
                    selvalue["id"] = selectionvalue.id
                    selvalue["name"] = selectionvalue.name
                    selvalue["odds"] = selectionvalue.odds
                    selectionsData.append(selvalue)
                value["selections"] = selectionsData
                marketData.append(value)
            Data["markets"] = marketData
            return Data
        else: # In case no event id is passed, this simply returns no data message.
            return {"id":"No data found for this Id."}

    def getDataByMatchName(self,MatchName): # This method is responsible to fetch data from DB using match name passed in URL of our defined API.
        Data = []
        evvalue = eventdetails.query.filter(eventdetails.name == MatchName).all()
        if len(evvalue) != 0: # This condition handles case when blank match name is passed in URL.
            for each in evvalue:
                value = {}
                value["id"]=each.id
                value["url"]="http://localhost:5000/api/match/"+str(each.id)
                value["name"]=each.name
                value["startTime"]=each.startTime.strftime("%Y-%m-%d %H:%M:%S")
                Data.append(value)
        else: # In case no match name is passed, this simply returns no data message.
            Data.append("No data for given match.")
        return Data

    def getDataByGameOrder(self,Game,Order): # This method is responsible to fetch data from DB using sport name and order passed in URL of our defined API.
        Data = []
        sportsvalue = sportsdetails.query.filter(sportsdetails.name == Game).all()
        if len(sportsvalue) != 0: # This condition handles case when blank parameters are passed in URL.
            for each in sportsvalue:
                evvalue = eventdetails.query.filter(eventdetails.sportId == each.id).order_by(desc(eventdetails.startTime)).all()
                for eachEValue in evvalue:
                    value = {}
                    value["id"]=eachEValue.id
                    url = "http://localhost:5000/api/match/"+str(eachEValue.id)
                    value["url"]=url
                    value["name"]=eachEValue.name
                    value["startTime"]=eachEValue.startTime.strftime("%Y-%m-%d %H:%M:%S")
                    Data.append(value)
        else: # In case no sport name and order is passed, this simply returns no data message.
            Data.append("No data for given sport and order.")
        return Data

    def AddData(self, Data): # This function is responsible to add new event data in database.
        try:
            mesvalue = messagedetails.query.filter(messagedetails.id == Data.get("id")).all()
            if len(mesvalue) != 0:
                return "Duplicate Entry"
            else:
                mes = messagedetails(id=Data.get("id"), message_type=Data.get("message_type"), Evid=Data.get("event").get("id"))
                db.session.add(mes)
                evvalue = eventdetails.query.filter(eventdetails.id == Data.get("event").get("id")).all()
                if len(evvalue) != 0:
                    return "Duplicate Entry"
                else:
                    ev = eventdetails(id=Data.get("event").get("id"), name=Data.get("event").get("name"), startTime=datetime.strptime(Data.get("event").get("startTime"), "%Y-%m-%d %H:%M:%S"),sportId=Data.get("event").get("sport").get("id"))
                    db.session.add(ev)
                    svalue = sportsdetails.query.filter(sportsdetails.id == Data.get("event").get("sport").get("id")).all()
                    if len(svalue) == 0:
                        sp = sportsdetails(id=Data.get("event").get("sport").get("id"),name=Data.get("event").get("sport").get("name"))
                        db.session.add(sp)
                    for market in Data.get("event").get("markets"):
                        mvalue = marketdetails.query.filter(marketdetails.id == market.get("id")).all()
                        evtom = evtomark(Evid=Data.get("event").get("id"), Mid=market.get("id"))
                        db.session.add(evtom)
                        if len(mvalue) == 0:
                            mark = marketdetails(id=market.get("id"),name=market.get("name"))
                            db.session.add(mark)
                        for selection in market.get("selections"):
                            marktos = marktosel(Mid=market.get("id"),Sid=selection.get("id"))
                            db.session.add(marktos)
                            selvalue = selectionsdetails.query.filter(selectionsdetails.id == selection.get("id")).all()
                            if len(selvalue) == 0:
                                sel = selectionsdetails(id=selection.get("id"), name=selection.get("name"), odds=selection.get("odds"))
                                db.session.add(sel)
                    db.session.commit()
                    return "Success"
        except:
            return "Failed"

    def UpdateData(self, Data): # This function is responsible to update odds in database.
        try:
            for market in Data.get("event").get("markets"):
                for selection in market.get("selections"):
                    selectionvalue = selectionsdetails.query.filter_by(id = selection.get("id")).first()
                    if selectionvalue != None:
                        db.session.execute(update(selectionsdetails).where(selectionsdetails.id == selection.get("id")).values(odds = selection.get("odds")))
                    else:
                        return "Failed"
            db.session.commit()
            return "Success"
        except:
            return "Failed"
