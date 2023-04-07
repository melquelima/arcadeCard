import os
from app import manager,app

os.environ["ENV"] = "CHARLE" #DEV ALEX
os.environ["INDEV"] = "1" #0

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    #app.run(host='0.0.0.0', port=port)#, use_reloader=False)
    
    manager.run()
    



    