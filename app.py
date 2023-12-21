from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS
from controllers.post_controller import post_bp
from controllers.instagram_controller import instagram_bp
from config.config import MONGODB_URI

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

app.config['MONGO_URI'] = MONGODB_URI
mongo = MongoClient(app.config['MONGO_URI'])
app.mongo = mongo['igcron']

app.register_blueprint(post_bp)
app.register_blueprint(instagram_bp)\

@app.route('/', methods=['GET'])
def home():
    return "Instagrapy-Server"

if __name__ == '__main__':
    app.run(debug=True, port=8080)