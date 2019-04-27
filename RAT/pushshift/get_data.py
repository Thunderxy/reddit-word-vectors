import requests
import json
from datetime import datetime
import pandas as pd


class Posts:

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
        html = requests.get(url)
        data = json.loads(html.text)    # {'data': [{'author': ' ', ...}, {'author': ' ', ...}, ..., n], ?: [], ...}
        if data:
            return data['data']
        else:
            return None

    def save_posts(self, file_name):
        data = []

        for i in range(self.n):
            my_url = self.make_url()
            data_ = Posts.get_from_pushshift(my_url)

            if data_:
                new_data = data + data_
                data = new_data

                self.before = data[-1]['created_utc']
                print('{} - {}'.format(i, from_timestamp(self.before)))
            else:
                break

        with open(file_name, 'w+') as f:
            json.dump(data, f)

        print('created: {}'.format(file_name))

    def get_DataFrame(self):
        """naredi pd.DataFrame iz .json lista
        if data=None => live, else: data=file => from saved file"""

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
        """Vzame .json kot list ter iz njega naredi listo Post objektov z danimi atributi."""

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
    """class, ki naredi objekt iz .json"""

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


def from_timestamp(unix_time):
    return datetime.fromtimestamp(int(unix_time))


# my_data = Posts(n=1, size=1000, sub='')
#
# my_data.save_posts('')
