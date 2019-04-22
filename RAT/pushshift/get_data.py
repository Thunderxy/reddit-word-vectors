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
        data = json.loads(html.text)
        return data['data']

    @staticmethod
    def from_timestamp(unix_time):
        return datetime.fromtimestamp(int(unix_time))

    def get_DataFrame(self):
        posts = pd.DataFrame(columns=['title', 'id', 'time'])

        for i in range(self.n):
            my_url = self.make_url()
            data = Posts.get_from_pushshift(my_url)

            self.before = data[-1]['created_utc']

            new_posts = pd.DataFrame({'title': post['title'], 'id': post['id'], 'time': Posts.from_timestamp(post['created_utc'])} for post in data)
            posts = pd.concat([posts, new_posts], ignore_index=True, sort=False)

        return posts


class Post(Posts):
    """subclass, ki naredi objekt iz .json fila"""

    def __init__(self, author, created_utc, post_id, num_comments, score, subreddit, title, **kwargs):
        super().__init__(**kwargs)
        self.author = author
        self.created_utc = created_utc
        self.post_id = post_id
        self.num_comments = num_comments
        self.score = score
        self.subreddit = subreddit
        self.title = title

    @staticmethod
    def get_post_list(data):
        """Vzame slovar (.json) ter iz njega naredi listo Post objektov z danimi atributi."""
        post_object_lst = []

        for post in data:
            post_object_lst.append(Post(post['author'], post['created_utc'], post['id'], post['num_comments'], post['score'], post['subreddit'], post['title']))

        return post_object_lst


# nacin brez razreda:

# def make_url(query, size, sort, after, before, sub):
#     url = 'https://api.pushshift.io/reddit/search/submission/?q={}&size={}&sort={}&after={}&before={}&subreddit={}'.format(query, size, sort, after, before, sub)
#     return url
#
#
# def get_from_pushshift(url):
#     html = requests.get(url)
#     data = json.loads(html.text)
#     return data['data']
#
#
# def from_timestamp(unix_time):
#     return datetime.fromtimestamp(int(unix_time))
#
#
# def get_mass_data(**kwargs):
#
#     n = kwargs.get('n', 1)
#     query = kwargs.get('q', '')
#     sort = kwargs.get('sort', 'desc')
#     size = kwargs.get('size', 25)
#     after = kwargs.get('after', '')
#     before = kwargs.get('before', '')
#     sub = kwargs.get('sub', '')
#
#     posts = pd.DataFrame(columns=['title', 'id', 'time'])
#
#     for i in range(n):
#         my_url = make_url(query, size, sort, after, before, sub)
#         data_ = get_from_pushshift(my_url)
#
#         before = data_[-1]['created_utc']
#
#         new_posts = pd.DataFrame({'title': post['title'], 'id': post['id'], 'time': from_timestamp(post['created_utc'])} for post in data_)
#         posts = pd.concat([posts, new_posts], ignore_index=True, sort=False)
#
#     return posts
#
#
# print(get_mass_data(sub='TheLastAirbender'))

my_data = Posts(size=3, sub='TheLastAirbender')

# subclass zadeva
# link = my_data.make_url()
# lst = my_data.get_from_pushshift(link)
# print([i.title for i in Post.get_post_list(lst)])

print(my_data.get_DataFrame())
