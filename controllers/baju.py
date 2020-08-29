from app import db
# from flask import jsonify
from conf.base import make_response, request, jwt_required, jsonify
from models import Baju

@jwt_required
def get_baju():
    try:
        baju = Baju.query.all()
        return jsonify([e.serialize() for e in baju])
    except Exception as e:
        return (str(e))

@jwt_required
def get_baju_by_id(id_):
    try:
        baju = Baju.query.filter_by(id = id_).first()
        return jsonify(baju.serialize())
    except Exception as e:
        return (str(e))

@jwt_required
def create_baju():
    post_data = request.get_json()
    if request.method == 'POST':
        try:
            baju = Baju(
                name = post_data.get('name'),
                size = post_data.get('size'),
                price = post_data.get('price'),
                quantity = post_data.get('quantity')
            )
            db.session.add(baju)
            db.session.commit()
            resp = {
                'status': 'success',
                'message': 'successfully insert'
            }
            return make_response(jsonify(resp)), 201
        except Exception as e:
            # return (str(e))
            resp = {
                'status': 'fail',
                'message': 'some error occured' + e
            }
            return make_response(jsonify(resp)), 401

@jwt_required
def update_baju(id):
    post_data = request.get_json()
    baju = Baju.query.filter_by(id = post_data.get('id')).first()
    if not baju:
        if not isinstance(str):
            try: 
                name = str(request.data.get('name', ''))
                baju.name = name
                db.session.add(baju)
                db.session.commit()
                resp = {
                    'id': baju.id,
                    'name': baju.name,
                    'size': baju.size,
                    'price': baju.price,
                    'quantity': baju.quantity
                }
                return jsonify(resp), 200
            except Exception as e:
                return(str(e))

@jwt_required
def delete_baju(id):
    post_data = request.get_json()
    baju = Baju.query.filter_by(id = post_data.get('id')).first()
    if not baju:
        if not isinstance(str):
            try:
                db.session.delete(baju)
                db.session.commit()
                return {
                    "message": "baju {} was deleted".format(baju.id)
                }
            except Exception as e:
                return (str(e))
