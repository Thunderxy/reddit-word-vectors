import json
import gzip
import os
import pandas as pd
from RAT.pushshift.get_data import Post, from_timestamp


def load_posts(file_name):
    with gzip.GzipFile(file_name) as f:
        json_bytes = f.read()

    json_str = json_bytes.decode('utf-8')
    data = json.loads(json_str)

    return data


def get_DataFrame(data):
    posts = pd.DataFrame({'title': post['title'], 'id': post['id'],
                          'time': from_timestamp(post['created_utc'])} for post in data)

    return posts


def get_post_list(data):
    post_object_lst = []

    for post in data:
        post_object_lst.append(Post.make_post_obj(post))

    return post_object_lst


def json_as_obj_lst(file_name):
    """Converts json to list of Post objects."""
    file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../pushshift/' + file_name)
    load = load_posts(file)
    return get_post_list(load)

# posts = load_posts('')
# posts_lst = get_post_list(posts)
