import os
os.environ["ENV"] = "CHARLE" #DEV ALEX
os.environ["INDEV"] = "0" #0


from app import app,SQLAlchemy,db


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run()