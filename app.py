import os
from flask import Flask, request, jsonify, abort, make_response, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, JWTManager)
# add queue lib
from rq import Queue
from rq.job import Job
from worker import conn

backserv = Flask(__name__)
backserv.config.from_object(os.environ['APP_SETTINGS'])
backserv.config['JWT_SECRET_KEY'] = 'Wh@tEv3r'
jwt = JWTManager(backserv)
backserv.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(backserv)
# add queue
q = Queue(connection=conn)

from controllers import controller
backserv.register_blueprint(controller)

# if __name__ == '__main__':
#     backserv.run(host='0.0.0.0', port='5000')