from flask import Blueprint, redirect, url_for, request,session,jsonify,make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
import uuid
from app import app, db
import jwt
import datetime
from functools import wraps

user_blueprint = Blueprint("user", __name__, template_folder="templates")

#Common function
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@user_blueprint.route("/user/", methods= ["GET"])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    users = User.query.all()
    output = []
    for user in users:
        output.append(user.serialize)
    return jsonify({'user' : output})


@user_blueprint.route("/user", methods= ["POST"])
@token_required 
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user:

        hashed_password = generate_password_hash(data['password'], method='sha256')
        public_id = str(uuid.uuid4())
        new_user = User(public_id=public_id, username=data['username'], password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'public_id' : public_id})

    else:
        return jsonify({'message' : 'Username already exsists'})


@user_blueprint.route("/user/<public_id>", methods = ["PUT"])
@token_required 
def change_password(current_user, public_id):
    if not current_user.public_id == public_id:
        return jsonify({'message' : 'Cannot perform that function!'})
    data = request.get_json()
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message' : 'No user found!'})

    hashed_password = generate_password_hash(data['password'], method='sha256')
    user.password = hashed_password
    db.session.commit()
    jsonify({'message' : 'Your password has been changed'})


@user_blueprint.route("/user/<public_id>", methods = ["GET"])
@token_required 
def get_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    return jsonify({'user' : user.serialize})



@user_blueprint.route("/user/me", methods = ["GET"])
@token_required 
def get_currect_user(current_user):
    return jsonify({'user' : current_user.serialize})



@user_blueprint.route("/user/<public_id>", methods = ["PUT"])
@token_required 
def edit_user(current_user, public_id):
    if not current_user.public_id == public_id and not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    data = request.get_json()
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    
    if 'admin'in data.keys():
        user.admin = (data['admin'].lower() == "true")
        print(data['admin'])

    if 'username'in data.keys():
        user.username = data['username']
    if 'first_name'in data.keys():
        user.first_name = data['first_name']
    if 'last_name'in data.keys():
        user.last_name = data['last_name']
    if 'email'in data.keys():
        user.email = data['email']
    if 'password'in data.keys():
        hashed_password = generate_password_hash(data['password'], method='sha256')
        user.password = hashed_password

    db.session.commit()
    

    return jsonify({'user' : user.serialize})

@user_blueprint.route("/user/<public_id>", methods = ["DELETE"])
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    user = User.query.filter_by(public_id=public_id).first()
    

    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})




@user_blueprint.route("/login", methods = ["POST"])
def login():
    auth = request.get_json()

    if not auth['username'] or not auth['password']:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth['username']).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth['password']):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

