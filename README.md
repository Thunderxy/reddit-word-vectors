# RAT (Reddit analysis tool)
Doing stuff with Reddit using https://pushshift.io/ and https://github.com/praw-dev/praw .


## Get posts with threading from pushshift and save them to .json.gz:
```Python
from RAT.pushshift.get_data_threading import LoggerConfig # optional
from RAT.pushshift.get_data_threading import GetPosts, SavePosts
from RAT.pushshift.classes import Posts

my_log = LoggerConfig(log_file='thread_log', level=logging.DEBUG, print_to_console=True) # optional
reddit_data = Posts(after=1559390400, size=1000, subreddit='askreddit')
posts = GetPosts(r_data, thread_num=5, max_per_sec=1, make_log=my_log).get_data() # data (posts) is global variable here
SavePosts('my_file.json.gz').save_posts()
```

## Loading posts from file:
```Python
from RAT.pushshift.load_data import FPosts

my_file = FPosts('my_file.json.gz')
my_posts = my_file.load_posts() # list of Post objects
```

### How to access post information from posts list
```Python
In [7]: titles = [i.title for i in my_posts]  
```
```
Out[7]: 
['Redditors who’ve forgiven a significant other that cheated, why did you forgive them?',
 'What are some of the unwritten rules followed by men/women?',
 '911 operators of Reddit, what was the most ridiculous thing anyone has called you for?',
 ...]
```

### Converting unix time to utc:
```Python
In [8]: from RAT.pushshift.classes import from_timestamp 
In [9]: created_utc = [from_timestamp(i.created_utc) for i in my_posts] 
In [10]: created_utc 
```
```
Out[10]: 
[datetime.datetime(2019, 5, 11, 18, 12, 43),
 datetime.datetime(2019, 5, 11, 18, 12, 43),
 datetime.datetime(2019, 5, 11, 18, 12, 41),
...]
```

https://github.com/pushshift/api for more info on parameters


## No threading version (obsolete):
```Python
from RAT.pushshift.get_data import get_post_list, get_DataFrame
from RAT.pushshift.classes import Posts
reddit_data = Posts(n=10, subreddit='askreddit') # gets n*25 new posts from r/askreddit
posts_df = get_DataFrame(reddit_data)
posts_lst = get_post_lst(reddit_data)

save_posts(reddit_data, 'my_file1.json.gz') # saving posts
```

# Content analysis
## Post comparison using tf and tf-idf
using posts from r/TheLastAirbender for example (~130000 total posts)

info: http://blog.christianperone.com/2013/09/machine-learning-cosine-similarity-for-vector-space-models-part-iii/
```Python
In [8]: from RAT.similarity.tfidf import tf_sim
In [9]: test_set = [i.title for i in Posts]   
In [10]: train_set = ['What happened to Aang (more specifically Raava) when Azula shot him with lightning?']
In [11]: sim_vec_tf = tf_sim(train_set, test_set)
In [12]: i_lst = get_matches(3, Posts, sim_vec_tf)    # also returns sorted index list
```
```
Vocabulary: {'happened': 2, 'aang': 0, 'specifically': 6, 'raava': 4, 'azula': 1, 'shot': 5, 'lightning': 3}
1.00 | 2019-04-26 02:09:42 | bhfu4l | What happened to Aang (more specifically Raava) when Azula shot him with lightning?
0.76 | 2018-02-26 00:34:24 | 808i00 |... but the ability was blocked when he was shot with Azula’s lightning.
0.65 | 2018-07-02 16:21:11 | 8vizzt | Aang has the scar from Azula's lightning in a scene that ...
```
```Python
In [13]: sim_vec_tfidf = tfidf_sim(train_set, test_set)
In [14]: get_matches(10, Posts, sim_vec_tfidf)
```
```
Vocabulary: {'happened': 2, 'aang': 0, 'specifically': 6, 'raava': 4, 'azula': 1, 'shot': 5, 'lightning': 3}
0.98 | 2019-04-26 02:09:42 | bhfu4l | What happened to Aang (more specifically Raava) when Azula shot him with lightning?
0.74 | 2018-02-26 00:34:24 | 808i00 | ... but the ability was blocked when he was shot with Azula’s lightning.
0.65 | 2013-09-21 00:18:16 | 1mszvf | What happened to the Waterbending Avatar from when Aang was killed by Azula?
```
note: different results, tfidf not the best for such sentance compariosn


## word2vec
https://radimrehurek.com/gensim/models/word2vec.html
using posts from r/TheLastAirbender for example (~130000 total posts)

### Text preprocessing
```Python
In [1]: from RAT.similarity.text_preprocessing import clean_posts   
In [2]: post_data = clean_posts(Posts)   # removed punctuation and tokenized
```
### Counting words
```Python
In [3]: from RAT.similarity.text_preprocessing import count_words
In [4]: count_words(post_data, sort=None)    # sort=True, returns list of tuples of most common words
```

### Pickiling post data
```Python
In [5]: from RAT.similarity.text_preprocessing import pickle_this
In [6]: pickle_this(post_data, 'data.pickle')
```

### Making word2vec model
```Python
In [1]: from RAT.similarity.word2vec import make_model  
In [2]: post_data = unpickle_this('data.pickle')
In [3]: my_model = make_model(post_data, size_=300, window_=2, min_count_=2, epochs_=5)
```

### Saving and loading word2vec model
```Python
In [5]: from RAT.similarity.word2vec import save_model, load_model 
In [5]: save_model('data.model', my_model)
In [6]: load_model('data.model')
```

### Testing word2vec model
```Python
print(my_model.wv.similarity('aang', 'zuko'))

for i in my_model.wv.most_similar(positive=['aang'], topn=10):
     print(i)

# both using cosine similarity
```
results:
```
0.5819699

('sokka', 0.6768596172332764)
('azula', 0.6717315912246704)
('toph', 0.6593050956726074)
('roku', 0.6275879144668579)
('katara', 0.612399697303772)
```

## Post comparsion using word2vec
### Summing word2vec vectors
```Python
In [1]: from RAT.similarity.add_word2vec import post_sim, most_similar
In [2]: post_data = unpickle_this('data.pickle')
In [3]: my_model = load_model('data.model')
In [4]: sim_nums = post_sim("My reaction to the cartoon vs my reaction to the movie", post_data, my_model)
In [5]: most_similar(sim_nums, post_data, 10)
```
results:
```
0: my reaction to the revelation
1: my reaction to the comedianamon meme
2: my reaction to the engagement rings
3: my reaction to the engagement rings
4: b4e13 my reaction to the ending
5: my response to the tla movie
6: b4e13 my response to the ending

reaction == response
```

### Using smooth inverse frequency
https://github.com/PrincetonML/SIF, 
https://github.com/peter3125/sentence2vec/blob/master/sentence2vec.py

```Python
In [1]: from RAT.similarity.sif_word2vec import post_sim, most_similar   
In [2]: from RAT.similarity.text_preprocessing import count_words
In [3]: post_data = unpickle_this('data.pickle')
In [4]: my_model = load_model('data.model')
In [5]: get_word_dct = count_words(post_data)    # word count for inverse frequency
In [6]: sim_nums = post_sim("My reaction to the cartoon vs my reaction to the movie", post_data, my_model, get_word_dct)
In [7]: most_similar(sim_nums, post_data)
```
results:
```
0: avatar the last airbender trailer reaction
1: avatar the last airbender how to end a cartoon part 3
2: avatar the last airbender how to end a cartoon part 1
3: fan content cartoon korra
4: the legend of korra as a 20s30sstyle cartoon
5: avatar the cartoon
6: no spoilers sokka is one of the best cartoon characters of all time
```
