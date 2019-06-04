import json
import gzip
import os
import pandas as pd
from RAT.pushshift.classes import Post, Comment, from_timestamp


class Content:
    """For loading saved files."""

    def __init__(self, file_name):
        self.file_name = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/' + file_name)

    def load_content_from_file(self):
        with gzip.GzipFile(self.file_name) as f:
            json_bytes = f.read()

        json_str = json_bytes.decode('utf-8')
        data = json.loads(json_str)

        return data

    @staticmethod
    def get_post_DataFrame(data):
        posts = pd.DataFrame({'title': post['title'], 'id': post['id'],
                              'time': from_timestamp(post['created_utc'])} for post in data)

        return posts

    @staticmethod
    def get_post_list(data):
        post_object_lst = []

        for post in data:
            post_object_lst.append(Post.make_post_obj(post))

        return post_object_lst

    @staticmethod
    def get_comment_list(data):
        comment_object_lst = []

        for comment in data:
            comment_object_lst.append(Comment.make_comment_obj(comment))

        return comment_object_lst

    def load_posts(self):
        """Loads posts as list of Post objects."""
        return self.get_post_list(self.load_content_from_file())

    def load_comments(self):
        """Loads comments as list of Comment objects."""
        return self.get_comment_list(self.load_content_from_file())
