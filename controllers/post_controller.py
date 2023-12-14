from flask import Blueprint, jsonify, request
from services.posts_service import get_all_posts, get_post, get_post_by_id, save_post, update_post, delete_post
from datetime import datetime

post_bp = Blueprint('main', __name__)

@post_bp.route('/<string:type>/<string:username>/all', methods=['GET'])
def all(type: str, username: str):
    try:
        posts = get_all_posts(type, username)
        return jsonify(posts), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })

@post_bp.route('/<string:type>/<string:username>', methods=['GET'])
def post(type: str, username: str):
    try:
        day = datetime.now().strftime('%d/%m/%Y')
        hour = request.args.get('hour')
        post = get_post(type, username, day, hour)
        return jsonify(post), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })

@post_bp.route('/<string:type>/<string:username>/<string:id>', methods=['GET'])
def post_by_id(type: str, username: str, id: str):
    try:
        post = get_post_by_id(type, username, id)
        return jsonify(post), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })
    
@post_bp.route('/<string:type>/<string:username>/add', methods=['POST'])
def add(type: str, username: str):
    try:
        body = request.get_json()
        post = save_post(type, username, body)
        return jsonify(post), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })
    
@post_bp.route('/<string:type>/update/<string:id>', methods=['PATCH'])
def update(type: str, id: str):
    try:
        body = request.get_json()
        updated = update_post(type, body, id)
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