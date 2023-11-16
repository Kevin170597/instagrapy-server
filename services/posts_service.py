from flask import current_app
from bson import ObjectId

def get_all_posts(type, username):
    db = current_app.mongo
    ig_posts = db['ig-posts']
    data = ig_posts.find({ 'type': type, 'username': username })
    data_list = [{**item, '_id': str(item['_id'])} for item in data]
    return data_list

def get_post(type, username, day, hour):
    db = current_app.mongo
    ig_posts = db['ig-posts']
    data = ig_posts.find_one({ 'type': type, 'username': username, 'day': day, 'hour': hour})
    data['_id'] = str(data['_id'])
    return data

def get_post_by_id(type, username, id):
    db = current_app.mongo
    ig_posts = db['ig-posts']
    data = ig_posts.find_one({ '_id': ObjectId(id), 'type': type, 'username': username })
    data['_id'] = str(data['_id'])
    return data

def save_post(post):
    db = current_app.mongo
    ig_posts = db['ig-posts']
    data = ig_posts.insert_one(post)
    return { '_id': str(data.inserted_id)}

def update_post(type, post, id):
    db = current_app.mongo
    ig_posts = db['ig-posts']
    data = ig_posts.update_one({ '_id': ObjectId(id), 'type': type }, { '$set': post })
    return { 'matched_count': data.matched_count, 'modified_count': data.modified_count }

def delete_post(type, id):
    db = current_app.mongo
    ig_posts = db['ig-posts']
    data = ig_posts.delete_one({ '_id': ObjectId(id), 'type': type })
    return { 'deleted_count': data.deleted_count }