"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# Routes
@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/signup', methods= ['POST'])
def handle_signup():
    email = request.json.get('email', None)
    first_name = request.json.get('firstname', None)
    last_name = request.json.get('lastname', None)
    password = request.json.get('password', None)
    verifypassword = request.json.get('verifypassword', None)
    newUser = User(email = email, password = password, first_name = first_name, last_name = last_name)
    if password != verifypassword:
        return jsonify('Passwords do not match'), 400
    if User.query.filter_by(email = email).first() == None:
        db.session.add(newUser)
        db.session.commit()
        return jsonify('Added User'), 200
    else:
        return jsonify('That email is already in use'), 400
    
@api.route('/login', methods=['POST'])
def handle_login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email = email, password=password).first()
    if user is None:
        return jsonify({"msg" : "Bad username or password"}), 401
    else:
        access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token, "user_id": user.id}), 200

@api.route('/home', methods=['GET'])
@jwt_required()
def handle_home():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user is not None:
        return jsonify({"user": user.serialize(), "status":"ok"}), 200
    else:
        return jsonify({'msg': 'You must be logged in'}), 400

@api.route('/groups', methods=['GET'])
@jwt_required()
def handle_get_groups():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user is not None:
        return jsonify(user.serialize()['groups']), 200
    else:
        return jsonify({'msg': 'You must be logged in'}), 400

@api.route('/groups', methods=['POST'])
@jwt_required()
def handle_add_group():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({"email":user.email, 'groups': groups}), 200

@api.route('/groups', methods=['DELETE'])
@jwt_required()
def handle_delete_group():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user is not None:
        groupList = Group.query.all()
        toDelete = None
        for item in groupList:
            if item.serialize()['name'] == name:
                toDelete = item
        if toDelete == None:
            return jsonify("invalid group id"), 400
        else:
            db.session.delete(toDelete)
            db.session.commit()
            return jsonify("group deleted"), 200
    else:
        return jsonify({'msg': 'You must be logged in'}), 400    

@api.route('/friends', methods=['GET'])
@jwt_required()
def handle_get_friends():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user is not None:
        return jsonify(user.serialize()['friends']), 200
    else:
        return jsonify({'msg': 'You must be logged in'}), 400

@api.route('/friends', methods=['POST'])
@jwt_required()
def handle_add_friend():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({"email":user.email, 'groups': groups}), 200

@api.route('/friends', methods=['DELETE'])
@jwt_required()
def handle_delete_friend():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user is not None:
        friendList = Friend.query.all()
        toDelete = None
        for item in friendList:
            if item.serialize()['name'] == name:
                toDelete = item
        if toDelete == None:
            return jsonify("invalid friend id"), 400
        else:
            db.session.delete(toDelete)
            db.session.commit()
            return jsonify("friend deleted"), 200
    else:
        return jsonify({'msg': 'You must be logged in'}), 400  
