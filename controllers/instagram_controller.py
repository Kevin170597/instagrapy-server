from flask import Blueprint, jsonify, request
from services.instagram_service import ig_login, post_album, post_photo, post_reel, post_story

instagram_bp = Blueprint('instagram', __name__)

def log_in():
    try:
        body = request.get_json()
        user = ig_login(body=body)
        return jsonify(user), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })

@instagram_bp.route('/instagram/photo/<string:username>', methods=['GET'])
def photo(username):
    try:
        posted = post_photo(username=username, hour=request.args.get('hour'))
        return jsonify(posted), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })

@instagram_bp.route('/instagram/album/<string:username>', methods=['GET'])
def album(username):
    try:
        posted = post_album(username=username, hour=request.args.get('hour'))
        return jsonify(posted), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })

@instagram_bp.route('/instagram/reel/<string:username>', methods=['GET'])
def reel(username):
    try:
        posted = post_reel(username=username, hour=request.args.get('hour'))
        return jsonify(posted), 200 
    except Exception as e:
        return jsonify({ 'error': str(e) })

@instagram_bp.route('/instagram/story/<string:username>', methods=['GET'])
def story(username):
    try:
        posted = post_story(username=username, hour=request.args.get('hour'))
        return jsonify(posted), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })


