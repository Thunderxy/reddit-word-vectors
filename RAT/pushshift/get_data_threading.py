import requests
import json
import gzip
import os
import time
import threading
import logging
from RAT.pushshift.classes import Posts, from_timestamp


s = requests.Session()
lock = threading.Lock()
data = []
api_calls = [0]
global_time = time.time()


def get_from_pushshift(url, thread_name):
    """Pulls data from pushshift API."""

    get_from = s.get(url)

    while get_from.status_code != 200:
        thread_log.warning('to many requests sleeping {}'.format(thread_name))
        time.sleep(5)

        try:
            get_from = s.get(url)
        except requests.exceptions.RequestException as e:
            thread_log.error('error in requests: {}'.format(e))
            get_from = 0

    ps_data = json.loads(get_from.text)
    if ps_data:
        return ps_data['data']
    else:
        return None


def thread_posts(posts_obj, thread_name, max_per_sec):
    """Main function for threading."""

    global data
    global api_calls

    n = posts_obj.n
    for i in range(n):
        throttler(thread_name, max_per_sec)
        api_calls[0] += 1

        start_time = time.time()

        my_url = posts_obj.make_url()
        data_ = get_from_pushshift(my_url, thread_name)

        if data_:
            data += data_
            posts_obj.before = data_[-1]['created_utc']
            thread_log.info('{} on cycle: {} | runtime: {} | last post date: {}'.format(thread_name, i, time.time() - start_time, from_timestamp(posts_obj.before)))
        else:
            break

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


def get_data(my_data, thread_num=5, max_per_sec=1):
    """Thread initialization function."""

    start_time = time.time()
    intervals = get_intervals(my_data, thread_num)
    threads_lst = []

    for i in range(thread_num):

        my_data_ = Posts(after=intervals[i][0], before=intervals[i][1], size=my_data.size, subreddit=my_data.sub, sort=my_data.sort)
        time.sleep(1)
        t = threading.Thread(target=thread_posts, name='thread{}'.format(i), args=(my_data_, 'thread{}'.format(i), max_per_sec))
        t.start()
        threads_lst.append(t)
        print('{} has started'.format(t.name))

    for t in threads_lst:
        t.join()

    print('total time: {} s\ntotal api calls: {}'.format(time.time() - start_time, api_calls[0]))
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


def throttler(thread_name, max_per_sec=1):
    """Throttles API connection."""

    global global_time

    lock.acquire()

    delta_t = time.time() - global_time
    limit = 1 / delta_t
    throttle_for = abs(2 - delta_t)     # better ideas?

    global_time = time.time()

    if limit > max_per_sec:
        thread_log.warning('{} @ {} calls/s, throttling for {} s'.format(thread_name, limit, throttle_for))
        lock.release()
        time.sleep(throttle_for)
    else:
        lock.release()


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


thread_log = setup_logger(log_file='thread_log', level=logging.DEBUG, print_to_console=True)


# r_data = Posts(after=1558699200, size=1000, subreddit='askreddit')
# get_data(r_data, 5, 1)
