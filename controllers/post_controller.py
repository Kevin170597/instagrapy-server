from flask import Blueprint, jsonify, request
from services.posts_service import get_all_posts, get_post, get_post_by_id, save_post, update_post, delete_post
from datetime import datetime

post_bp = Blueprint('main', __name__)

@post_bp.route('/<type>/<username>/all', methods=['GET'])
def all(type, username):
    try:
        posts = get_all_posts(type, username)
        return jsonify(posts), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })

@post_bp.route('/<type>/<username>', methods=['GET'])
def post(type, username):
    try:
        day = datetime.now().strftime('%d/%m/%Y')
        hour = request.args.get('hour')
        post = get_post(type, username, day, hour)
        return jsonify(post), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })

@post_bp.route('/<type>/<username>/<id>', methods=['GET'])
def post_by_id(type, username, id):
    try:
        post = get_post_by_id(type, username, id)
        return jsonify(post), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })
    
@post_bp.route('/<type>/add', methods=['POST'])
def add(type):
    try:
        body = request.get_json()
        body['type'] = type
        post = save_post(body)
        return jsonify(post), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })
    
@post_bp.route('/<type>/update/<id>', methods=['PATCH'])
def update(type, id):
    try:
        body = request.get_json()
        updated = update_post(type, body, id)
        return jsonify(updated), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })
    
@post_bp.route('/<type>/delete/<id>', methods=['DELETE'])
def delete(type, id):
    try:
        deleted = delete_post(type, id)
        return jsonify(deleted), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })