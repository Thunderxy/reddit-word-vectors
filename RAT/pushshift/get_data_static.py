import json
import pandas as pd
from datetime import datetime
from RAT.pushshift.get_data_live import Post


def from_timestamp(unix_time):
    return datetime.fromtimestamp(int(unix_time))


def load_posts(file_name):
    with open(file_name) as f:
        data = json.load(f)

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


# posts = load_posts('atla_all.json')
