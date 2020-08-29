from flask import Blueprint
from controllers.baju import get_baju, get_baju_by_id, update_baju, create_baju, delete_baju
from controllers.user import reg_user, login_user, update_user

controller = Blueprint('controller', 'controllers', url_prefix='/api')
controller.add_url_rule('/registration', view_func=reg_user, methods=['POST'])
controller.add_url_rule('/login', view_func=login_user, methods=['POST'])
controller.add_url_rule('/user/:id', view_func=update_user, methods=['PUT'])

controller.add_url_rule('/baju', view_func=get_baju, methods=['GET'])
controller.add_url_rule('/baju', view_func=create_baju, methods=['POST'])
controller.add_url_rule('/baju/:id', view_func=update_baju, methods=['PUT'])
controller.add_url_rule('/baju/:id', view_func=get_baju_by_id, methods=['GET'])
controller.add_url_rule('/baju/:id', view_func=delete_baju, methods=['DELETE'])