import json
import gzip
import os
import pandas as pd
from RAT.pushshift.classes import Post, from_timestamp


class FPosts:
    """File Posts for loading saved files."""

    def __init__(self, file_name):
        self.file_name = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/' + file_name)

    def load_posts_from_file(self):
        with gzip.GzipFile(self.file_name) as f:
            json_bytes = f.read()

        json_str = json_bytes.decode('utf-8')
        data = json.loads(json_str)

        return data

    @staticmethod
    def get_DataFrame(data):
        posts = pd.DataFrame({'title': post['title'], 'id': post['id'],
                              'time': from_timestamp(post['created_utc'])} for post in data)

        return posts

    @staticmethod
    def get_posts_list(data):
        post_object_lst = []

        for post in data:
            post_object_lst.append(Post.make_post_obj(post))

        return post_object_lst

    def load_posts(self):
        """Loads posts as list of Post objects."""
        return self.get_posts_list(self.load_posts_from_file())
