import pyodbc 

DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
CORS_HEADERS = 'Content-Type'
SECRET_KEY = "asdjkgasd$#43"

SERVER = "arcadeserver.database.windows.net" 
DB = "arcadecard" 
USER = "arcadeAdmin" 
PWD = "qwerty333#" 

drivers = [item for item in pyodbc.drivers()] 
driverH = drivers[-1]
driver = "SQL+Server"
print("driver:{}".format(driver)) 

SQLALCHEMY_DATABASE_URI     = f"mssql+pyodbc://{USER}:{PWD}@{SERVER}/{DB}?driver={driver}"
SQLALCHEMY_DATABASE_HEROKU = f"mssql+pyodbc://{USER}:{PWD}@{SERVER}/{DB}?driver={driverH}" 
SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_HEROKU

#SQLALCHEMY_DATABASE_URI = "sqlite:///storage.db"
#SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://loginmaster:qwerty333#@arcadecard2.database.windows.net/principal?driver=SQL+Server"