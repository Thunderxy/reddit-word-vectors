import requests
import json
import gzip
import os
import pandas as pd
import time
from RAT.pushshift.classes import Post, timestamp_to_utc


s = requests.Session()


def get_from_pushshift(url):
    """Pulls data from pushshift API."""

    html = s.get(url)
    data = json.loads(html.text)
    if data:
        return data['data']
    else:
        return None


def save_posts(my_data, file_name):
    """Saves posts from pushshift. No threading version."""

    data = []

    for i in range(my_data.n):
        start = time.time()
        my_url = my_data.make_url()
        data_ = get_from_pushshift(my_url)

        if data_:
            new_data = data + data_
            data = new_data

            my_data.before = data[-1]['created_utc']
            print('{} - {} @ {} s'.format(i, timestamp_to_utc(my_data.before), time.time() - start))
        else:
            break

    json_str = json.dumps(data)
    json_bytes = json_str.encode('utf-8')

    file_name_ = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/' + file_name)
    with gzip.GzipFile(file_name_, 'w+') as f:
        f.write(json_bytes)

    print('created: {}'.format(file_name))


def get_DataFrame(my_data):
    """Makes Pandas DataFrame from posts."""

    posts = pd.DataFrame(columns=['title', 'id', 'time'])

    for i in range(my_data.n):
        my_url = my_data.make_url()
        data = get_from_pushshift(my_url)

        if data:
            my_data.before = data[-1]['created_utc']
            new_posts = pd.DataFrame({'title': post['title'], 'id': post['id'], 'time': timestamp_to_utc(post['created_utc'])} for post in data)
            posts = pd.concat([posts, new_posts], ignore_index=True, sort=False)
            print('on date: {}'.format(timestamp_to_utc(my_data.before)))
        else:
            break

    return posts


def get_posts_list(my_data):

    post_object_lst = []

    for i in range(my_data.n):
        my_url = my_data.make_url()
        data = get_from_pushshift(my_url)

        if data:
            my_data.before = data[-1]['created_utc']
            print('on date: {}'.format(timestamp_to_utc(my_data.before)))
            for post in data:
                post_object_lst.append(Post.make_post_obj(post))
        else:
            break

    return post_object_lst


def get_posts_gen(my_data):

    while True:
        my_url = my_data.make_url()
        data = get_from_pushshift(my_url)

        post_object_lst = []

        if data:
            my_data.before = data[-1]['created_utc']
            for post in data:
                post_object_lst.append(Post.make_post_obj(post))
        else:
            break

        yield post_object_lst
