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


class GetPosts:

    def __init__(self, posts, thread_num=1, max_per_sec=1, make_log=False):
        self.posts = posts
        self.thread_num = thread_num
        self.max_per_sec = max_per_sec

        if make_log:
            self.thread_log = make_log.setup_logger()
        else:
            self.thread_log = logging.getLogger()
            self.thread_log.disabled = True

    def get_data(self):
        """Thread initialization function."""

        start_time = time.time()
        intervals = self.get_intervals()
        threads_lst = []

        for i in range(self.thread_num):
            my_data_ = Posts(after=intervals[i][0], before=intervals[i][1], size=self.posts.size, subreddit=self.posts.sub, sort=self.posts.sort)
            t = threading.Thread(target=self.thread_posts, name='thread{}'.format(i), args=(my_data_, 'thread{}'.format(i)))
            time.sleep(1 / self.max_per_sec)
            t.start()
            threads_lst.append(t)
            print('{} has started'.format(t.name))

        for t in threads_lst:
            t.join()

        print('total time: {} s\ntotal api calls: {}'.format(time.time() - start_time, api_calls[0]))
        return data

    def get_intervals(self):
        """Make time intervals."""

        t1 = int(self.posts.after)
        t2 = int(self.posts.before)
        delta_t = int((t2 - t1) / self.thread_num)

        intervals = []
        for i in range(self.thread_num):
            intervals.append([t1 + delta_t * i, t1 + delta_t * (i + 1) - 1])

        return intervals

    def thread_posts(self, i_posts, thread_name):
        """Main function for threading."""

        global data
        global api_calls

        n = self.posts.n
        for i in range(n):
            self.throttler(thread_name)
            api_calls[0] += 1

            start_time = time.time()

            my_url = i_posts.make_url()
            data_ = self.get_from_pushshift(my_url, thread_name)

            if data_:
                with lock:
                    data += data_

                i_posts.before = data_[-1]['created_utc']
                self.thread_log.info('{} on cycle: {} | runtime: {} | last post date: {}'.format(thread_name, i, time.time() - start_time, from_timestamp(i_posts.before)))
            else:
                break

        self.thread_log.info('{} done'.format(thread_name))

    def get_from_pushshift(self, url, thread_name):
        """Pulls data from pushshift API."""

        get_from = s.get(url)

        while get_from.status_code != 200:
            self.thread_log.warning('to many requests sleeping {}'.format(thread_name))
            time.sleep(5)

            try:
                get_from = s.get(url)
            except requests.exceptions.RequestException as e:
                self.thread_log.error('error in requests: {}'.format(e))
                get_from = 0

        ps_data = json.loads(get_from.text)
        if ps_data:
            return ps_data['data']
        else:
            return None

    def throttler(self, thread_name):
        """Throttles API connection."""

        global global_time

        lock.acquire()

        delta_t = time.time() - global_time
        limit = 1 / delta_t
        throttle_for = abs((1 / self.max_per_sec) - delta_t)

        global_time = time.time()

        if limit > self.max_per_sec:
            self.thread_log.warning('{} over limit by {} calls/s, throttling for {} s'.format(thread_name, limit - self.max_per_sec, throttle_for))
            time.sleep(throttle_for)
            lock.release()
        else:
            lock.release()


class LoggerConfig:

    def __init__(self, name=__name__, log_file='threads.log', level=logging.DEBUG, log_format='%(asctime)s: %(levelname)s: %(message)s', print_to_console=False):
        self.name = name
        self.log_file = log_file
        self.level = level
        self.log_format = log_format
        self.print_to_console = print_to_console

    def setup_logger(self):

        try:
            os.remove(self.log_file)
        except OSError:
            pass

        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)

        formatter = logging.Formatter(self.log_format)

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        if self.print_to_console:
            logging.debug('')

        return logger


class SavePosts:

    def __init__(self, file_name):
        self.file_name = file_name

    def save_posts(self):
        """Saves data to file_name.json.gz ."""

        global data

        logging.info('saving to file...')

        json_str = json.dumps(data)
        json_bytes = json_str.encode('utf-8')

        file_name_ = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/' + self.file_name)
        with gzip.GzipFile(file_name_, 'w+') as f:
            f.write(json_bytes)

        print('created: {}'.format(self.file_name))
