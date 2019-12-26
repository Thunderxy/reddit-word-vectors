import requests
import json
import gzip
import os
import time
import threading
import logging
import datetime
from RAT.pushshift.classes import Posts, Comments


class GetContent:

    def __init__(self, after, subreddit, content, before=time.time(), size=1000, thread_num=1, max_per_sec=1, log_level='warning'):
        """
        Parameters
        ----------
        thread_num: int
            Number of threads to be used.
        max_per_sec: float
            API call limit.
        log_level: None or DEBUG, INFO, WARNING

        Other Parameters
        ----------------
        data
        s
        lock
        api_calls
        global_time

        """
        self.after = after
        self.before = before
        self.content = content
        self.subreddit = subreddit

        if size > 1000:
            raise ValueError('max size is 1000.')
        else:
            self.size = size

        self.thread_num = thread_num
        self.max_per_sec = max_per_sec

        self.data = []
        self.s = requests.Session()
        self.lock = threading.Lock()
        self.api_calls = 0
        self.global_time = time.time()

        if log_level:
            logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=log_level.upper())

    def get_intervals(self):
        """ Make time intervals. """

        t1 = int(self.after)
        t2 = int(self.before)
        delta_t = int((t2 - t1) / self.thread_num)

        intervals = []
        for i in range(self.thread_num):
            intervals.append([t1 + delta_t * i, t1 + delta_t * (i + 1) - 1])

        return intervals

    def get_content(self):
        """ Thread initialization function. """

        start_time = time.time()
        intervals = self.get_intervals()
        threads_lst = []

        for i in range(self.thread_num):
            if self.content == 'post':
                my_data = Posts(after=intervals[i][0], before=intervals[i][1], size=self.size, subreddit=self.subreddit)
            elif self.content == 'comment':
                my_data = Comments(after=intervals[i][0], before=intervals[i][1], size=self.size, subreddit=self.subreddit)
            else:
                raise NameError

            t = threading.Thread(target=self.thread_content, name='thread_{}'.format(i), args=(my_data, 'thread_{}'.format(i)))
            time.sleep(1 / self.max_per_sec)
            t.start()
            threads_lst.append(t)
            logging.info('{} has started\n'.format(t.name))

        for t in threads_lst:
            t.join()

        logging.info('total time: {:.2f} s\n'.format(time.time() - start_time))
        logging.info('total api calls: {}\n'.format(self.api_calls))
        logging.info('number of posts/comments collected: {}\n'.format(len(self.data)))
        time.sleep(1)

        return self

    def thread_content(self, iter_content, thread_name):
        """ Main function for threading.

        Parameters
        ----------
        iter_content: class
            Helper class. Remembers after, before and has make_url method.
        thread_name: str
            Name of thread running this method.

        Returns
        -------
        None when done.

        """
        c = 0
        while True:
            self.throttler(thread_name)

            start_time = time.time()

            my_url = iter_content.make_url()
            data_ = self.get_from_pushshift(my_url, thread_name)

            if data_:
                with self.lock:
                    self.data += data_
                    self.api_calls += 1

                iter_content.before = data_[-1]['created_utc']

                logging.debug('{} on cycle: {} | runtime: {:.2f} s | after: {} | before: {}\n'.format(thread_name, c,
                              time.time() - start_time, timestamp_to_utc(iter_content.after),
                              timestamp_to_utc(iter_content.before)))
            else:
                break

            c += 1

        logging.info('{} done\n'.format(thread_name))

        return None

    def get_from_pushshift(self, url, thread_name):
        """ Pulls data from pushshift API. """

        get_from = self.s.get(url)

        while get_from.status_code != 200:
            logging.warning('to many requests sleeping {}\n'.format(thread_name))
            time.sleep(5)

            try:
                get_from = self.s.get(url)
            except requests.exceptions.RequestException as e:
                logging.error('error in requests: {}\n'.format(e))
                get_from = 0

        ps_data = json.loads(get_from.text)
        if ps_data:
            return ps_data['data']
        else:
            return None

    def throttler(self, thread_name):
        """ Throttles API connection. """

        self.lock.acquire()

        delta_t = time.time() - self.global_time
        limit = 1 / delta_t
        throttle_for = abs((1 / self.max_per_sec) - delta_t)

        self.global_time = time.time()

        if limit > self.max_per_sec:
            logging.info('{} over limit by {:.2f} calls/s, throttling for {:.2f} s\n'.format(thread_name, limit - self.max_per_sec, throttle_for))
            time.sleep(throttle_for)
            self.lock.release()
        else:
            self.lock.release()

    def save_content(self, file_name):
        """ Saves data to file_name.json.gz. """

        logging.info('saving to file...\n')

        json_str = json.dumps(self.data)
        json_bytes = json_str.encode('utf-8')

        file_name += '.json.gz'

        file_name_ = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/reddit_data/' + file_name)
        with gzip.GzipFile(file_name_, 'w+') as f:
            f.write(json_bytes)

        logging.info('created: {}\n'.format(file_name))

        return True


def timestamp_to_utc(timestamp):
    """timestamp -> utc time
       print(timestamp_to_utc('1576022400'))"""
    return datetime.datetime.utcfromtimestamp(int(timestamp))


def utc_to_timestamp(utc_time):
    """utc_time -> timestamp
       print(utc_to_timestamp('2019-12-11 00:00:00'))"""
    return int(datetime.datetime.strptime(utc_time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone.utc).timestamp())


if __name__ == '__main__':

    def get_from_reddit(after_, before_, subreddit, size):

        a = GetContent(after=after_, before=before_, subreddit=subreddit,
                       size=size, content='comment', thread_num=2, max_per_sec=1, log_level='info').get_content()

        for dct in a.data:
            print(dct['body'])

        a.save_content('my_first_save')


    get_from_reddit(time.time()-1000, time.time(), 'askreddit', 1000)
