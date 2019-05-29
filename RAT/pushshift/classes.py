import time
import sys
from datetime import datetime


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
    """

    def __init__(self, n=sys.maxsize, query='', sort='desc', size=25, after=0, before=int(time.time()), subreddit=''):
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


class Post:
    """Makes Post from dict (json)."""

    def __init__(self, author, created_utc, post_id, num_comments, score, subreddit, title, selftext):
        self.author = author
        self.created_utc = created_utc
        self.post_id = post_id
        self.num_comments = num_comments
        self.score = score
        self.subreddit = subreddit
        self.title = title
        self.selftext = selftext

    @staticmethod
    def make_post_obj(post):
        return Post(post['author'], post['created_utc'], post['id'], post['num_comments'], post['score'], post['subreddit'], post['title'], post['selftext'])


def from_timestamp(unix_time):
    """unix time -> utc time"""
    return datetime.fromtimestamp(int(unix_time))
