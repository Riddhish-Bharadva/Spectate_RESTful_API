# Below class is responsible to create Database and tables in case program runs for the first time in system.
class CreateDBStructure:
    def CreateDatabase(self, Con): # Function to create database in MySQL database.
        try:
            DBCursor = Con.cursor()
            DBCursor.execute("create database spectateTest;")
            return "Database created successfully."
        except:
            return "Error occurred while creating a new database. It either exist or there are some connection issues."
    def CreateTables(self, Con): # Function to create all the required tables in MySQL database.
        try:
            DBCursor = Con.cursor()
            DBCursor.execute("create table messagedetails(id bigint PRIMARY KEY, message_type varchar(25), EvId bigint);")
            DBCursor.execute("create table eventdetails(id bigint PRIMARY KEY, name varchar(25), startTime datetime(6), sportId int);")
            DBCursor.execute("create table sportsdetails(id int PRIMARY KEY, name varchar(25));")
            DBCursor.execute("create table evtomark(Evid bigint, Mid bigint, PRIMARY KEY(Evid,Mid));")
            DBCursor.execute("create table marketdetails(id bigint PRIMARY KEY, name varchar(25));")
            DBCursor.execute("create table marktosel(Mid bigint, Sid bigint, PRIMARY KEY(Mid,Sid));")
            DBCursor.execute("create table selectionsdetails(id bigint PRIMARY KEY, name varchar(25), odds float(50));")
            return "Tables created successfully."
        except:
            return "Error occurred while creating a new tables. One of them either exist or there are some connection issues."
