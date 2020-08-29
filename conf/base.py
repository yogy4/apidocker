from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
from flask import Flask, Blueprint, request, jsonify, render_template, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, JWTManager)
# from controllers.pengguna import test
# from psycopg2 import *
# from app import db
# apl = Flask(__name__)
# from controllers.pengguna import test

tampilan = Flask(__name__)
tampilan.config.from_object(os.environ['APP_SETTINGS'])
tampilan.config['JWT_SECRET_KEY'] = 'somestri1!ng'
jwt = JWTManager(tampilan)
tampilan.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# tampilan.register_blueprint(controller)
db = SQLAlchemy(tampilan)
base = Blueprint('base', 'base')