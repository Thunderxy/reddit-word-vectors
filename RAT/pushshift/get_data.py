import requests
import json
import gzip
import os
from datetime import datetime
import pandas as pd
from time import time


class Posts:
    """Makes Posts object from pushshift link."""

    s = requests.Session()

    def __init__(self, n=1, query='', sort='desc', size=1, after='', before='', sub=''):
        self.n = n
        self.query = query
        self.sort = sort
        self.size = size
        self.after = after
        self.before = before
        self.sub = sub

    def make_url(self):
        url = 'https://api.pushshift.io/reddit/search/submission/?q={}&size={}&sort={}&after={}&before={}&subreddit={}'.format(self.query, self.size, self.sort, self.after, self.before, self.sub)
        return url

    @staticmethod
    def get_from_pushshift(url):
        html = Posts.s.get(url)
        data = json.loads(html.text)    # {'data': [{'author': ' ', ...}, {'author': ' ', ...}, ..., n], ?: [], ...}
        if data:
            return data['data']
        else:
            return None

    def save_posts(self, file_name):
        """Saves Posts from pushshift to .json.gz ."""
        data = []

        for i in range(self.n):
            start = time()
            my_url = self.make_url()
            data_ = Posts.get_from_pushshift(my_url)

            if data_:
                new_data = data + data_
                data = new_data

                self.before = data[-1]['created_utc']
                print('{} - {} @ {} s'.format(i, from_timestamp(self.before), time() - start))
            else:
                break

        json_str = json.dumps(data)
        json_bytes = json_str.encode('utf-8')

        file_name_ = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/' + file_name)
        with gzip.GzipFile(file_name_, 'w+') as f:
            f.write(json_bytes)

        print('created: {}'.format(file_name))

    def get_DataFrame(self):
        """Makes pd.DataFrame from Posts (works live)."""

        posts = pd.DataFrame(columns=['title', 'id', 'time'])

        for i in range(self.n):
            my_url = self.make_url()
            data = Posts.get_from_pushshift(my_url)

            if data:
                self.before = data[-1]['created_utc']
                new_posts = pd.DataFrame({'title': post['title'], 'id': post['id'],
                                          'time': from_timestamp(post['created_utc'])} for post in data)
                posts = pd.concat([posts, new_posts], ignore_index=True, sort=False)
            else:
                break

        return posts

    def get_post_list(self):
        """Makes list of objects Post and saves them to list (works live)."""

        post_object_lst = []

        for i in range(self.n):
            my_url = self.make_url()
            data = Posts.get_from_pushshift(my_url)

            if data:
                self.before = data[-1]['created_utc']
                for post in data:
                    post_object_lst.append(Post.make_post_obj(post))
            else:
                break

        return post_object_lst


class Post:
    """Makes Post from dict (json)."""

    def __init__(self, author, created_utc, post_id, num_comments, score, subreddit, title):
        self.author = author
        self.created_utc = created_utc
        self.post_id = post_id
        self.num_comments = num_comments
        self.score = score
        self.subreddit = subreddit
        self.title = title

    @staticmethod
    def make_post_obj(post):
        return Post(post['author'], post['created_utc'], post['id'], post['num_comments'], post['score'], post['subreddit'], post['title'])


class fPosts:
    """Loading saved file."""

    def __init__(self, file_name):
        self.file_name = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/' + file_name)

    def load_posts(self):
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


def from_timestamp(unix_time):
    """unix time -> utc time"""
    return datetime.fromtimestamp(int(unix_time))
