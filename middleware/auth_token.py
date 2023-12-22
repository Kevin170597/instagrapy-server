from functools import wraps
from flask import request, jsonify
import jwt
from config.config import JWT_SECRET_ENCODER, JWT_ALGORITHM

def auth_middleware(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({ 'error': 'Token is missing.' }), 400
        
        try:
            data = jwt.decode(token, JWT_SECRET_ENCODER, algorithms=JWT_ALGORITHM)
            userid = data['userid']
        except:
            return jsonify({
                'message': 'Token is invalid.'
            }), 401
        
        return f(userid, *args, **kwargs)
    
    return decorated