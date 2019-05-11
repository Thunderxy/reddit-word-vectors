# RAT (Reddit analysis tool)
Doing stuff with Reddit using https://pushshift.io/ and https://github.com/praw-dev/praw .


## Working without saving posts
### How to get posts from reddit using https://pushshift.io/
```Python
In [1]: from RAT.pushshift.get_data import Posts
In [2]: my_data = Posts(n=1, size=25, sub='askreddit')     
```


### Get posts in list format or in DataFrame format
```Python
In [3]: Posts_lst=my_data.get_post_list()    
In [4]: Posts_df=my_data.get_DataFrame() 
In [5]: Posts_lst 
```

```
Out[5]: 
[<RAT.pushshift.get_data.Post at 0x7f7de778deb8>,
 <RAT.pushshift.get_data.Post at 0x7f7de778d198>,
 <RAT.pushshift.get_data.Post at 0x7f7de778d0f0>,
...]
```

```Python
In [6]: Posts_df   
```

```
Out[6]: 
                                               title      id                time
0   Teens of reddit whats the most rebellious thin...  bndqa8 2019-05-11 18:10:20
1            Where is the most upvoted "F" on reddit?  bndq9r 2019-05-11 18:10:18
2   What was the worst way you figured out you wer...  bndq5d 2019-05-11 18:10:03
3                                        Just Curious  bndq4o 2019-05-11 18:10:01
4   [NSFW] The fellas of Reddit, what desperate si...  bndq4a 2019-05-11 18:09:59
...
```


### How to access post information from Posts object
```Python
In [7]: titles = [i.title for i in Posts_lst]  
```
```
Out[7]: 
['Redditors who’ve forgiven a significant other that cheated, why did you forgive them?',
 'What are some of the unwritten rules followed by men/women?',
 '911 operators of Reddit, what was the most ridiculous thing anyone has called you for?',
 ...]
 # posts are different from Posts_df beacuse r/askreddit gets alot of new conetent and we only looked at 25 new ones
```

#### Converting unix time to utc:
```Python
In [8]: from RAT.pushshift.get_data import from_timestamp 
In [9]: created_utc = [from_timestamp(i.created_utc) for i in Posts_lst] 
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



## Working with saved posts
### Saving posts to .json.gz
```Python
In [1]: from RAT.pushshift.get_data import Posts
In [2]: my_data = Posts(n=1, size=25, sub='askreddit')
In [3]: my_data.save_posts('askreddit_data.json.gz')    # saves .json from pushshift
```

### Loading saved posts
```Python
In [4]: from RAT.pushshift.get_data import fPosts   
In [5]: my_file = fPosts('askreddit.json.gz')                                                                                                          
In [6]: Posts = my_file.get_posts_list(my_file.load_posts())     # load file and convert it to list of Post objects
In [7]: Posts
```
```
Out[7]: 
[<RAT.pushshift.get_data.Post at 0x7f568f782080>,
 <RAT.pushshift.get_data.Post at 0x7f568f7829e8>,
 <RAT.pushshift.get_data.Post at 0x7f568f6c04a8>,
...]
```


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
#### Pickiling post data
```Python
In [3]: from RAT.similarity.text_preprocessing import pickle_this
In [4]: pickle_this(post_data, 'data.pickle')
```

### Making word2vec model
```Python
In [1]: from RAT.similarity.word2vec import make_model  
In [2]: post_data = unpickle_this('data.pickle')
In [3]: my_model = make_model(post_data, size_=300, window_=2, min_count_=2, epochs_=5)
```

### Saving word2vec model
```Python
In [4]: save_model('data.model', my_model)
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
