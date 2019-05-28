import requests
import json
import gzip
import os
import time
import threading
import logging
from RAT.pushshift.classes import Posts, from_timestamp

s = requests.Session()
data = []
api_calls = 0
start_time = 0


def get_from_pushshift(url, thread_name):
    """Pulls data from pushshift API."""

    get_from = s.get(url)

    while get_from.status_code != 200:
        thread_log.warning('to many requests sleeping {}'.format(thread_name))
        time.sleep(5)
        get_from = s.get(url)

    ps_data = json.loads(get_from.text)
    if ps_data:
        return ps_data['data']
    else:
        return None


def thread_posts(posts_obj, thread_name):
    """Main function for threading."""

    global data

    n = posts_obj.n
    for i in range(n):
        start = time.time()

        my_url = posts_obj.make_url()
        data_ = get_from_pushshift(my_url, thread_name)

        if data_:
            data += data_
            posts_obj.before = data_[-1]['created_utc']
            thread_log.info('{} on cycle: {} | runtime: {} | last post date: {}'.format(thread_name, i, time.time() - start, from_timestamp(posts_obj.before)))
        else:
            break

        throttler(thread_name)

    thread_log.info('{} done'.format(thread_name))


def get_intervals(my_data, n):
    """Make time intervals."""

    t1 = int(my_data.after)
    t2 = int(my_data.before)
    delta_t = int((t2 - t1) / n)

    intervals = []
    for i in range(n):
        intervals.append([t1 + delta_t*i, t1 + delta_t*(i+1) - 1])

    return intervals


def get_data(my_data, thread_num=1):
    """Thread initialization function."""

    global start_time
    start_time = time.time()
    intervals = get_intervals(my_data, thread_num)
    threads_lst = []

    for i in range(thread_num):

        my_data_ = Posts(after=intervals[i][0], before=intervals[i][1], size=my_data.size, subreddit=my_data.sub, sort=my_data.sort)

        t = threading.Thread(target=thread_posts, name='thread{}'.format(i), args=(my_data_, 'thread{}'.format(i)))
        t.start()
        threads_lst.append(t)
        print('{} has started'.format(t.name))

    for t in threads_lst:
        t.join()

    print('total time: {} s'.format(time.time() - start_time))
    return data


def save_posts(file_name):
    """Saves data to file_name.json.gz ."""

    global data

    logging.info('saving to file...')

    json_str = json.dumps(data)
    json_bytes = json_str.encode('utf-8')

    file_name_ = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/' + file_name)
    with gzip.GzipFile(file_name_, 'w+') as f:
        f.write(json_bytes)

    print('created: {}'.format(file_name))


def throttler(thread_name):
    """Throttles API connection."""
    # TODO fix this

    global api_calls
    api_calls += 1

    limit = api_calls / (time.time() - start_time)

    if limit > 1:
        thread_log.warning('{} @ {} calls/s, throttling'.format(thread_name, limit))
        time.sleep(5)


def setup_logger(name=__name__, log_file='name.log', level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s', print_to_console=False):

    try:
        os.remove(log_file)
    except OSError:
        pass

    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(format)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    if print_to_console:
        logging.debug('')

    return logger


# thread_log = setup_logger(log_file='thread_log', level=logging.DEBUG, print_to_console=True)
#
#
# r_data = Posts(after=1558699200, size=1000, subreddit='askreddit')
# get_data(r_data, 5)
