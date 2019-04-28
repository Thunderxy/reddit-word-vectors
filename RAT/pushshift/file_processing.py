import json
import pandas as pd
from RAT.pushshift.get_data import Post, from_timestamp


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


# posts = load_posts('')
# posts_lst = get_post_list(posts)
