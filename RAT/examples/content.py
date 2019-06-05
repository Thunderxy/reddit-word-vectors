from RAT.pushshift.get_data_threading import GetContent, LoggerConfig, SaveContent
from RAT.pushshift.classes import Comments, timestamp_to_utc
import logging
import time


def get_from_reddit(n, after_, before_):
    my_log = LoggerConfig(log_file='thread_log{}'.format(n), level=logging.DEBUG, print_to_console=True)
    reddit_comments = Comments(after=after_, before=before_, size=1000, subreddit='askreddit')
    GetContent(reddit_comments, thread_num=3, max_per_sec=1, make_log=my_log).get_content()
    SaveContent('askreddit_comments{}.json.gz'.format(n)).save_content()
    time.sleep(1)


def chunk_it(days, per_day):
    delta_t = 24 * 60 * 60 * per_day
    now = int(time.time())

    t2 = now
    for i in range(days):
        t1 = now - (i + 1) * delta_t
        get_from_reddit(i, t1, t2)
        t2 = t1

        print(timestamp_to_utc(t1))


chunk_it(5, 1)
