DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
CORS_HEADERS = 'Content-Type'
SECRET_KEY = "asdjkgasd$#43"



import urllib
params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 10.0};SERVER=loginmaster:qwerty333#@arcadecard2.database.windows.net/principal")


#SQLALCHEMY_DATABASE_URI = "sqlite:///storage.db"
SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://loginmaster:qwerty333#@arcadecard2.database.windows.net/principal?driver=SQL+Server+Native+Client+11.0"