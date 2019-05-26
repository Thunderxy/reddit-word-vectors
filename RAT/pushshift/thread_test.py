import requests
import json
import gzip
import os
from datetime import datetime
import time
import threading
import logging

s = requests.Session()
data = []
api_calls = 0
start_time = 0


class Posts:
    """Creates Posts object from pushshift link.

    Note:
        n or time must be specified.

    Args:
        n: Number of API calls.
        query: Not supported (look at pushshift docs).
        sort: Descending or ascending. Defaults to 'desc'.
        size: Number of objects in API call (max 1000 per call).
        after(int): Unix timestamp.
        before(int): Unix timestamp.
        subreddit: Subreddit, if '' then r/all.

    TODO: Do something with 1e12.
    """

    def __init__(self, n=int(1e12), query='', sort='desc', size=25, after=0, before=int(time.time()), subreddit=''):
        self.n = n
        self.query = query
        self.sort = sort
        self.size = size
        self.after = after
        self.before = before
        self.sub = subreddit

    def make_url(self):
        url = 'https://api.pushshift.io/reddit/search/submission/?q={}&size={}&sort={}&after={}&before={}&subreddit={}'.format(self.query, self.size, self.sort, self.after, self.before, self.sub)
        return url


def get_from_pushshift(url, thread_name):
    """Pulls data from pushshift API.

    Args:
        url: Address for accessing API. From Posts.make_url().
        thread_name: Name of thread.

    Returns:
        Json data from API.
        None if API returns [].
    """
    get_from = s.get(url)

    while get_from.status_code != 200:
        logging.warning('to many requests, sleeping {}'.format(thread_name))
        time.sleep(5)
        get_from = s.get(url)

    ps_data = json.loads(get_from.text)
    if ps_data:
        return ps_data['data']
    else:
        return None


def thread_posts(posts_obj, thread_name):
    """Main function for threading.

    Gets url from Posts object and uses get_from_pushshift to get data. If data then gets last time from json and
    continuous from there. If not data then breaks.

    Note:
        Saves all json data to global data list.

    Args:
        posts_obj: Posts.
        thread_name: Name of thread.

    Returns:
        None

    """
    global data

    n = posts_obj.n
    for i in range(n):
        start = time.time()

        my_url = posts_obj.make_url()
        data_ = get_from_pushshift(my_url, thread_name)

        if data_:
            data += data_
            posts_obj.before = data_[-1]['created_utc']
            print('cycle: {} on {} - {} @ {} s'.format(i, thread_name, from_timestamp(posts_obj.before), time.time() - start))
        else:
            break

        throttler(thread_name)

    print('\n{} has finished\n'.format(thread_name))


def get_data(my_data, thread_num=1):
    """Thread initialization function.

    Makes thread_num of threads. Gives each thread a Posts object with different time intervals.

    Args:
        my_data: Posts object.
        thread_num: Number of given threads.

    Returns:
        data: All data gathered from API.

    """
    global start_time
    start = time.time()
    intervals = get_intervals(my_data, thread_num)
    threads_lst = []

    for i in range(thread_num):

        my_data_ = Posts(after=intervals[i][0], before=intervals[i][1], size=my_data.size, subreddit=my_data.sub, sort=my_data.sort)

        t = threading.Thread(target=thread_posts, name='thread {}'.format(i), args=(my_data_, 'thread {}'.format(i)))
        t.start()
        threads_lst.append(t)
        print('{} has started'.format(t.name))
        time.sleep(3)

    start_time = time.time()

    for t in threads_lst:
        t.join()

    print('total time: {} s'.format(time.time() - start))
    return data


def get_intervals(my_data, n):
    """Make time intervals.

    Given after and before make equidistant time intervals.

    Args:
        my_data: Posts object with after/before.
        n: Number of threads.

    Returns:
        intervals: n equidistant intervals.

    """

    t1 = int(my_data.after)
    t2 = int(my_data.before)
    delta_t = int((t2 - t1) / n)

    intervals = []
    for i in range(n):
        intervals.append([t1 + delta_t*i, t1 + delta_t*(i+1) - 1])

    return intervals


def save_posts(file_name):
    """Saves data to file_name.json.gz .

    Args:
        file_name: File name.

    Returns:
        None

    """
    global data

    logging.info('saving to file...')

    json_str = json.dumps(data)
    json_bytes = json_str.encode('utf-8')

    file_name_ = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/' + file_name)
    with gzip.GzipFile(file_name_, 'w+') as f:
        f.write(json_bytes)

    print('created: {}'.format(file_name))


def from_timestamp(unix_time):
    """unix time -> utc time"""
    return datetime.fromtimestamp(int(unix_time))


def throttler(thread_name):
    """Throttles API connection.

    Sleeps threads if api_calls/s > 1.5 .

    Args:
        thread_name: Thread name.

    Returns:
        None

    """
    global api_calls
    api_calls += 1

    limit = api_calls / (time.time() - start_time)

    if limit > 1.5:
        logging.warning('limit @ {} calls/s - sleeping {}'.format(limit, thread_name))
        time.sleep(5)
