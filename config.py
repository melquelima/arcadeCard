import pyodbc 
import os

DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
CORS_HEADERS = 'Content-Type'
SECRET_KEY = "asdjkgasd$#43"


ENV = os.environ.get('ENV', 'NULL')
INDEV = os.environ.get('DEV', '0')

print(ENV,INDEV)

if ENV == 'ALEX':
    SERVER = "arcadeserver.database.windows.net" 
    DB = "arcadecard" 
    USER = "arcadeAdmin" 
    PWD = "qwerty333#" 
elif ENV == 'CHARLE':
    SERVER = "arcadeserv.database.windows.net" 
    DB = "arcadebd"  
    USER = "adminarcade" 
    PWD = "Qwerty333#" 


if INDEV == '1':
    drivers = [item for item in pyodbc.drivers()] 
    driver = drivers[-1]
else:
    driver = "SQL+Server"
    driver = "ODBC Driver 17 for SQL Server"



print("driver:{}".format(driver)) 

SQLALCHEMY_DATABASE_URI     = f"mssql+pyodbc://{USER}:{PWD}@{SERVER}/{DB}?driver={driver}"
#SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_HEROKU

#SQLALCHEMY_DATABASE_URI = "sqlite:///storage.db"
#SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://loginmaster:qwerty333#@arcadecard2.database.windows.net/principal?driver=SQL+Server"