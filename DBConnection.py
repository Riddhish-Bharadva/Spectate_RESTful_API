from UserAndDBDetails import *
import mysql.connector

# Below class and method is responsible to create database connectivity by passing username, password, host and db name where applicable.
class DBConnect:
    def Connect(self,DBName): # This function creates db connection and returns the same for further CRUD operations.
        try:
            if DBName == "None": # If DB name is not passed in this function, MySQL DB connection is created without database selection.
                Con = mysql.connector.connect(host=host,user=username,password=password,auth_plugin="mysql_native_password")
            else: # If DB name is passed while calling this function, MySQL DB connection is created and passed database is selected.
                Con = mysql.connector.connect(host=host,user=username,password=password,auth_plugin="mysql_native_password",database=DBName)
            return Con
        except:
            return "Error occurred while connecting to MySQL DB."
