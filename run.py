import os

from app import manager,app


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    #app.run(host='0.0.0.0', port=port)#, use_reloader=False)
    app.run(host='0.0.0.0', port=port)
    
    #manager.run()
    



    