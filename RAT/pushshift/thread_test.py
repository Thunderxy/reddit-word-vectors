import requests
import json
import gzip
import os
from datetime import datetime
import time
import threading

s = requests.Session()
data = []
api_calls = 0
start_time = 0


class Posts:
    """Makes Posts object from pushshift link."""

    def __init__(self, n=int(1e12), query='', sort='desc', size=25, after=0, before=int(time.time()), sub=''):
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


def get_from_pushshift(url):
    html = s.get(url)
    ps_data = json.loads(html.text)    # {'data': [{'author': ' ', ...}, {'author': ' ', ...}, ..., n], ?: [], ...}
    if ps_data:
        return ps_data['data']
    else:
        return None


def thread_posts(posts_obj, thread_name):
    global data

    n = posts_obj.n
    for i in range(n):
        start = time.time()

        my_url = posts_obj.make_url()
        data_ = get_from_pushshift(my_url)

        if data_:
            data.append(data_)
            posts_obj.before = data_[-1]['created_utc']
            print('cycle: {} on {} - {} @ {} s'.format(i, thread_name, from_timestamp(posts_obj.before), time.time() - start))
        else:
            break

        throttler()

    return '{} has finished'.format(thread_name)


def save_posts(file_name):
    global data

    json_str = json.dumps(data)
    json_bytes = json_str.encode('utf-8')

    file_name_ = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/' + file_name)
    with gzip.GzipFile(file_name_, 'w+') as f:
        f.write(json_bytes)

    print('created: {}'.format(file_name))

    return True


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


def from_timestamp(unix_time):
    """unix time -> utc time"""
    return datetime.fromtimestamp(int(unix_time))


def get_intervals(my_data, n):
    before = int(my_data.before)
    after = int(my_data.after)

    dist = int((before - after) / n)

    intervals = []
    after_ = after
    for i in range(n):
        intervals.append(int(after_))
        after_ += dist

    return intervals


def thread_data(my_data, thread_num=1):
    global start_time
    start = time.time()
    intervals = get_intervals(my_data, thread_num)
    threads_lst = []

    for i in range(thread_num):

        if i == thread_num - 1:
            my_data_ = Posts(after=intervals[i], before=my_data.before, size=my_data.size, sub='askreddit')
            t = threading.Thread(target=thread_posts, name='thread {}'.format(i), args=(my_data_, 'thread {}'.format(i)))
            print('created thread {}'.format(i))
        else:
            my_data_ = Posts(after=intervals[0], before=intervals[1], size=my_data.size, sub='askreddit')
            t = threading.Thread(target=thread_posts, name='thread {}'.format(i), args=(my_data_, 'thread {}'.format(i)))
            print('created thread {}'.format(i))

        t.start()
        threads_lst.append(t)
        print('{} has started'.format(t.name))

    start_time = time.time()

    for t in threads_lst:
        t.join()

    print('total time: {} s'.format(time.time() - start))
    return data


def throttler():
    global api_calls
    api_calls += 1

    limit = api_calls / (time.time() - start_time)

    if limit > 3:
        print('limit @ {} calls/s - slowing down'.format(limit))
        time.sleep(5)


r_data = Posts(after=1558699200, size=1000, sub='askreddit')
thread_data(r_data, 10)

save_posts('threads.json.gz')

# TODO fix time bug in intervals and after, before in threading
