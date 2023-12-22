from typing import Optional

class Post:
    def __init__(
            self, 
            day: str, 
            hour: str, 
            posted: bool, 
            type: str, 
            username: str, 
            userid: str,
            url: str = None, 
            urls: list = None,
            caption: str = None
        ):
        self.day = day
        self.hour = hour
        self.posted = posted
        self.type = type
        self.username = username
        self.userid = userid
        self.url = url
        self.urls = urls
        self.caption = caption

    def to_dict(self):
        return {
            'day': self.day,
            'hour': self.hour,
            'posted': self.posted,
            'type': self.type,
            'username': self.username,
            'userid': self.userid,
            'url': self.url,
            'urls': self.urls,
            'caption': self.caption
        }