from RAT.pushshift.get_data_threading import GetContent, LoggerConfig, SaveContent
from RAT.pushshift.classes import Comments
import logging


my_log = LoggerConfig(log_file='thread_log', level=logging.DEBUG, print_to_console=True)

reddit_comments = Comments(after=1559660400, size=1000, subreddit='askreddit')
comments = GetContent(reddit_comments, thread_num=3, max_per_sec=1, make_log=my_log).get_content()
SaveContent('askreddit_comments.json.gz').save_content()
