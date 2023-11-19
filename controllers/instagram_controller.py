from flask import Blueprint, jsonify, request
from datetime import datetime
from services.posts_service import get_post
import requests
from instagrapi import Client
import os
from config.config import BULLWORTHPICS_PASSWORD

instagram_bp = Blueprint('instagram', __name__)

@instagram_bp.route('/instagram/login', methods=['GET'])
def log_in():
    try:
        body = request.get_json()
        if 'username' in body and 'password' in body:
            username = body['username']
            password = body['password']
        cl = Client()
        user = cl.login(username, password)
        if user == True:
            user_info = cl.user_info_by_username('bullworth.pics').dict()
            return jsonify(user_info), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })
    
@instagram_bp.route('/instagram/reel/<username>', methods=['GET'])
def reel(username):
    try:
        password = BULLWORTHPICS_PASSWORD
        day = datetime.now().strftime('%d/%m/%Y')
        hour = request.args.get('hour')

        data = get_post('reel', username, day, hour)
        data['_id'] = str(data['_id'])

        thumbnail = requests.get(data['thumbnail'])
        reel = requests.get(data['url'], stream=True)

        thumbnail_filename = data['thumbnail'].split('/')[-1]
        reel_filename = data['url'].split('/')[-1]

        with open(f'./downloads/{thumbnail_filename}', 'wb') as thumbnail_file:
            thumbnail_file.write(thumbnail.content)
        with open(f'./downloads/{reel_filename}', 'wb') as reel_file:
            reel_file.write(reel.content)

        cl = Client()
        cl.login(username, password)

        cl.clip_upload(f'.downloads/{reel_filename}', data['caption'], thumbnail)

        os.remove(f'./downloads/{thumbnail_filename}')
        os.remove(f'./downloads/{reel_filename}')

        return jsonify(username, day, hour), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })

@instagram_bp.route('/instagram/album/<username>', methods=['GET'])
def album(username):
    try:
        password = BULLWORTHPICS_PASSWORD
        day = datetime.now().strftime('%d/%m/%Y')
        hour = request.args.get('hour')

        data = get_post('album', username, day, hour)
        data['_id'] = str(data['_id'])

        files_paths = []

        for url in data['urls']:
            req_image = requests.get(url)
            filename = url.split('/')[-1]
            with open(f'./downloads/{filename}', 'wb') as file:
                file.write(req_image.content)
            files_paths.append(f'./downloads/{filename}')

        cl = Client()
        cl.login(username, password)

        cl.album_upload(files_paths, data['caption'])

        for path in files_paths:
            os.remove(path)

        return jsonify(username, day, hour), 200
    except Exception as e:
        return jsonify({ 'error': str(e) })