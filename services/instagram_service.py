import os
import requests
from datetime import datetime
from instagrapi import Client
import jwt
from config.config import BULLWORTHPICS_PASSWORD, JWT_SECRET_ENCODER, JWT_ALGORITHM
from services.posts_service import get_post, update_post

def ig_login(body):
    username = ''
    password = ''
    if 'username' in body and 'password' in body:
        username = body['username']
        password = body['password']
    cl = Client()
    try: 
        user = cl.login(username, password)
    except Exception as e:
        user = False
    user_info = []
    if user == True:
        user_info = cl.user_info_by_username(username).dict()
        token = jwt.encode({ 'userid': user_info['pk'] }, JWT_SECRET_ENCODER, algorithm=JWT_ALGORITHM)
        user_info['token'] = token
    else:
        raise ValueError("Invalid username or password")
    return user_info

def post_photo(username: str, hour: str, userid: str):
    password = BULLWORTHPICS_PASSWORD
    day = datetime.now().strftime('%d/%m/%Y')

    data = get_post('photo', username, day, hour, userid)
    data['_id'] = str(data['_id'])
    
    photo = requests.get(data['url'])
    filename = data['url'].split('/')[-1]
    with open(f'./downloads/{filename}', 'wb') as file:
        file.write(photo.content)

    cl = Client()
    cl.login(username, password)
    cl.photo_upload(f'./downloads/{filename}', data['caption'])
    
    os.remove(f'./downloads/{filename}')

    update_post('photo', { 'posted': True }, data['_id'], userid)

    return { 'username': username, 'day': day, 'hour': hour }

def post_album(username: str, hour: str, userid: str):
    password = BULLWORTHPICS_PASSWORD
    day = datetime.now().strftime('%d/%m/%Y')

    data = get_post('album', username, day, hour, userid)
    data['_id'] = str(data['_id'])

    files_paths = []

    for url in data['urls']:
        album = requests.get(url)
        filename = url.split('/')[-1]
        with open(f'./downloads/{filename}', 'wb') as file:
            file.write(album.content)
        files_paths.append(f'./downloads/{filename}')

    cl = Client()
    cl.login(username, password)
    cl.album_upload(files_paths, data['caption'])

    for path in files_paths:
        os.remove(path)

    update_post('album', { 'posted': True }, data['_id'], userid)

    return { 'username': username, 'day': day, 'hour': hour }

def post_reel(username, hour, userid: str):
    password = BULLWORTHPICS_PASSWORD
    day = datetime.now().strftime('%d/%m/%Y')

    data = get_post('reel', username, day, hour, userid)
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

    cl.clip_upload(f'.downloads/{reel_filename}', data['caption'], f'./downloads/{thumbnail_filename}')

    os.remove(f'./downloads/{thumbnail_filename}')
    os.remove(f'./downloads/{reel_filename}')

    update_post('reel', { 'posted': True }, data['_id'], userid)

    return { 'username': username, 'day': day, 'hour': hour }

def post_story(username, hour, userid: str):
    password = BULLWORTHPICS_PASSWORD
    day = datetime.now().strftime('%d/%m/%Y')

    data = get_post('story', username, day, hour, userid)
    data['_id'] = str(data['_id'])

    story = requests.get(data['url'])
    filename = data['url'].split('/')[-1]
    with open(f'./downloads/{filename}', 'wb') as file:
        file.write(story.content)            

    cl = Client()
    cl.login(username, password)
    cl.photo_upload_to_story(f'./downloads/{filename}')

    os.remove(f'./downloads/{filename}')
    
    update_post('story', { 'posted': True }, data['_id'], userid)

    return { 'username': username, 'day': day, 'hour': hour }




