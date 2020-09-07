# from app import backserv
from manage import manager, backserv

app_serv = backserv
if __name__ == '__main__':
    # app.run()
    app_serv.run()