from flask import Blueprint, jsonify, request
from services.posts_service import get_all_posts, get_post, get_post_by_id, save_post, update_post, delete_post
from datetime import datetime
from middleware.auth_token import auth_middleware

post_bp = Blueprint('main', __name__)

@post_bp.route('/<string:type>/<string:username>/all', methods=['GET'])
@auth_middleware
def all(auth_result: str, type: str, username: str):
    try:
        if auth_result == username:
            posts = get_all_posts(type, auth_result)
            return jsonify(posts), 200
        else: 
            raise ValueError('Token is invalid.')
    except Exception as e:
        return jsonify({ 'error': str(e) })

@post_bp.route('/<string:type>/<string:username>', methods=['GET'])
@auth_middleware
def post(auth_result: str, type: str, username: str):
    try:
        if auth_result == username:
            day = datetime.now().strftime('%d/%m/%Y')
            hour = request.args.get('hour')
            post = get_post(type, username, day, hour)
            return jsonify(post), 200
        else: 
            raise ValueError('Token is invalid.')
    except Exception as e:
        return jsonify({ 'error': str(e) })

@post_bp.route('/<string:type>/<string:username>/<string:id>', methods=['GET'])
@auth_middleware
def post_by_id(auth_result: str, type: str, username: str, id: str):
    try:
        if auth_result == username:
            post = get_post_by_id(type, username, id)
            return jsonify(post), 200
        else: 
            raise ValueError('Token is invalid.')
    except Exception as e:
        return jsonify({ 'error': str(e) })
    
@post_bp.route('/<string:type>/<string:username>/add', methods=['POST'])
@auth_middleware
def add(auth_result: str, type: str, username: str):
    try:
        if auth_result == username:
            body = request.get_json()
            post = save_post(type, username, body)
            return jsonify(post), 200
        else: 
            raise ValueError('Token is invalid.')
    except Exception as e:
        return jsonify({ 'error': str(e) })
    
@post_bp.route('/<string:type>/update/<string:id>', methods=['PATCH'])
@auth_middleware
def update(auth_result: str, type: str, id: str):
    try:
        if auth_result:
            body = request.get_json()
            updated = update_post(type, body, id)
            return jsonify(updated), 200
        else: 
            raise ValueError('Token is invalid.')
    except Exception as e:
        return jsonify({ 'error': str(e) })
    
@post_bp.route('/<string:type>/delete/<string:id>', methods=['DELETE'])
def delete(type: str, id: str):
    try:
        deleted = delete_post(type, id)
        return jsonify(deleted), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })