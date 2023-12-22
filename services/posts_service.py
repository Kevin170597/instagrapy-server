from flask import current_app
from bson import ObjectId
from models.post_model import Post

def validate_type(type: str):
    valid_types = ['album', 'photo', 'story', 'reel']
    if type not in valid_types:
        raise ValueError(f'{type} is not a valid type.')

def get_all_posts(type: str, username: str):
    validate_type(type)
    db = current_app.mongo
    ig_posts = db['ig-posts']
    data = ig_posts.find({ 'type': type, 'username': username, 'posted': { '$ne': True } })
    data_list = [{**item, '_id': str(item['_id'])} for item in data][::-1]
    return data_list

def get_post(type: str, username: str, day: str, hour: str):
    validate_type(type)
    db = current_app.mongo
    ig_posts = db['ig-posts']
    data = ig_posts.find_one({ 'type': type, 'username': username, 'day': day, 'hour': hour})
    data['_id'] = str(data['_id'])
    return data

def get_post_by_id(type: str, username: str, id: str):
    validate_type(type)
    db = current_app.mongo
    ig_posts = db['ig-posts']
    data = ig_posts.find_one({ '_id': ObjectId(id), 'type': type, 'username': username })
    data['_id'] = str(data['_id'])
    return data

def save_post(type: str, username: str, post):
    validate_type(type)
    db = current_app.mongo
    ig_posts = db['ig-posts']
    post_data = Post(
        day=post['day'], 
        hour=post['hour'], 
        posted=False, 
        type=type, 
        username=username, 
        url=post.get('url'), 
        urls=post.get('urls'),
        caption=post.get('caption')
    )
    data = ig_posts.insert_one(post_data.to_dict())
    return { '_id': str(data.inserted_id)}

def update_post(type: str, post, id: str):
    validate_type(type)
    db = current_app.mongo
    ig_posts = db['ig-posts']
    data = ig_posts.update_one({ '_id': ObjectId(id), 'type': type }, { '$set': post })
    return { '_id': id }

def delete_post(type: str, id: str):
    validate_type(type)
    db = current_app.mongo
    ig_posts = db['ig-posts']
    data = ig_posts.delete_one({ '_id': ObjectId(id), 'type': type })
    return { 'deleted_count': data.deleted_count }
