from typing import Optional

class Post:
    def __init__(self, 
                caption: str, 
                day: str, 
                hour: str, 
                posted: bool, 
                type: str, 
                username: str, 
                url: str = None, 
                urls: list = None):
        self.caption = caption
        self.day = day
        self.hour = hour
        self.posted = posted
        self.type = type
        self.username = username
        self.url = url
        self.urls = urls

    def to_dict(self):
        return {
            'caption': self.caption,
            'day': self.day,
            'hour': self.hour,
            'posted': self.posted,
            'type': self.type,
            'username': self.username,
            'url': self.url,
            'urls': self.urls
        }