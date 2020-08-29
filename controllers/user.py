from app import db
from conf.base import make_response, request, create_access_token, jwt_required, jsonify
from models import User

def reg_user():
    data = request.get_json()
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'message': 'Email {} already exists'.format(data['email'])})
    new_user = User(
        # id = kode,
        name = data['name'],
        email = data['email'],
        avatar = data['avatar_url'],
        password = User.generate_hash(data['password'])
    )
    try:
        
        new_user.save_to_db()
        access_token = create_access_token(identity = data['email'])
        return jsonify({
            'message': 'Email {} was created'.format(data['email']),
            'access token': access_token
        }), 201
    except:
        return jsonify({'message': 'something wrong'}), 500

def login_user():
    data = request.get_json()
    current_user = User.query.filter_by(email=data.get('email')).first()
    if not current_user:
        return jsonify({'message': 'Email {} doesn\'t exists'.format(data['email'])}), 404
    if User.verify_hash(data['password'], current_user.password):
        access_token = create_access_token(identity = data['email'])
        return jsonify({
            'message': 'Logged as {}'.format(current_user.email),
            'access token': access_token
        }), 200
    else:
        return jsonify({'message': 'wrong credentials'}), 404

@jwt_required
def update_user(id):
    post_data = request.get_json()
    pengguna = User.query.filter_by(id = post_data.get('id')).first()
    if not pengguna:
        if not isinstance(str):
            try:
                avatar = str(request.data.get('avatar_url', ''))
                pengguna.avatar = avatar
                db.session.add(avatar)
                db.session.commit()
                resp = {
                    'id': pengguna.id,
                    'name': pengguna.name,
                    'email': pengguna.email,
                    'avatar': pengguna.avatar,
                    'password': pengguna.password
                }
                return jsonify(resp), 200
            except Exception as e:
                return (str(e))