from flask import Blueprint, jsonify, request
from services.posts_service import get_all_posts, get_post, get_post_by_id, save_post, update_post, delete_post
from datetime import datetime
from middleware.auth_token import auth_middleware

post_bp = Blueprint('main', __name__)

@post_bp.route('/<string:type>/<string:username>/all', methods=['GET'])
@auth_middleware
def all(userid: str, type: str, username: str):
    try:
        posts = get_all_posts(type, username, userid)
        return jsonify(posts), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })

@post_bp.route('/<string:type>/<string:username>', methods=['GET'])
@auth_middleware
def post(userid: str, type: str, username: str):
    try:
        day = datetime.now().strftime('%d/%m/%Y')
        hour = request.args.get('hour')
        post = get_post(type, username, day, hour, userid)
        return jsonify(post), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })

@post_bp.route('/<string:type>/<string:username>/<string:id>', methods=['GET'])
@auth_middleware
def post_by_id(userid: str, type: str, username: str, id: str):
    try:
        post = get_post_by_id(type, username, id, userid)
        return jsonify(post), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })
    
@post_bp.route('/<string:type>/<string:username>/add', methods=['POST'])
@auth_middleware
def add(userid: str, type: str, username: str):
    try:
        body = request.get_json()
        post = save_post(type, username, body, userid)
        return jsonify(post), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })
    
@post_bp.route('/<string:type>/update/<string:id>', methods=['PATCH'])
@auth_middleware
def update(userid: str, type: str, id: str):
    try:
        body = request.get_json()
        updated = update_post(type, body, id, userid)
        return jsonify(updated), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })
    
@post_bp.route('/<string:type>/delete/<string:id>', methods=['DELETE'])
def delete(type: str, id: str):
    try:
        deleted = delete_post(type, id)
        return jsonify(deleted), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })