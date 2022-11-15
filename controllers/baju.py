from app import db
# from flask import jsonify
from conf.base import make_response, request, jwt_required, jsonify
from app import Job
from worker import conn
import operator
from app import q
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

@jwt_required
def create_with_queue():
    if request.method == "POST":
        job = q.enqueue_call(func=create_baju, result_ttl=5000)
        print(job.get_id())

@jwt_required
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        result = Baju.query.filter_by_id(id=job.result).first()
        results = sorted(result.result_no_stop_word.items(), key=operator.itemgetter(1), reverse=True)[:10]
        return jsonify(results)
    else:
        return "Nay", 202

