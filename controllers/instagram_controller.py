from flask import Blueprint, jsonify, request
from datetime import datetime
from services.posts_service import get_post
import requests
from instagrapi import Client
import os
from config.config import BULLWORTHPICS_PASSWORD

instagram_bp = Blueprint('instagram', __name__)

@instagram_bp.route('/instagram/album/<username>')
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

        return jsonify(username, day, hour)
    except Exception as e:
        return jsonify({ 'error': str(e) })