# RAT (Reddit analysis tool)
Doing stuff with Reddit using https://pushshift.io/ and https://github.com/praw-dev/praw .

### How to get posts from reddit
```Python
In [1]: from RAT.pushshift.get_data import Posts
In [2]: my_data = Posts(n=1, size=25, sub='askreddit')     
```

### Get posts in list format or in DataFrame format
```Python
In [3]: Posts_lst=my_data.get_post_list()    
In [4]: Posts_df=my_data.get_DataFrame() 

In [5]: Posts_lst 
Out[5]: 
[<RAT.pushshift.get_data.Post at 0x7f7de778deb8>,
 <RAT.pushshift.get_data.Post at 0x7f7de778d198>,
 <RAT.pushshift.get_data.Post at 0x7f7de778d0f0>,
...]

In [6]: Posts_df   
Out[6]: 
[                                               title      id                time
0   Teens of reddit whats the most rebellious thin...  bndqa8 2019-05-11 18:10:20
1            Where is the most upvoted "F" on reddit?  bndq9r 2019-05-11 18:10:18
2   What was the worst way you figured out you wer...  bndq5d 2019-05-11 18:10:03
3                                        Just Curious  bndq4o 2019-05-11 18:10:01
4   [NSFW] The fellas of Reddit, what desperate si...  bndq4a 2019-05-11 18:09:59
...]
```

### How to access post information from Posts object
```Python
In [7]: titles = [i.title for i in Posts_lst]  
Out[7]: 
['Redditors who’ve forgiven a significant other that cheated, why did you forgive them?',
 'What are some of the unwritten rules followed by men/women?',
 '911 operators of Reddit, what was the most ridiculous thing anyone has called you for?',
 ...]
 # posts are different from Posts_df beacuse r/askreddit gets alot of new conetent and we only looked at 25 new ones
```
converting unix time to utc:
```Python
In [8]: from RAT.pushshift.get_data import from_timestamp 
In [9]: created_utc = [from_timestamp(i.created_utc) for i in Posts_lst] 
In [10]: created_utc                                                                                                                                   
Out[10]: 
[datetime.datetime(2019, 5, 11, 18, 12, 43),
 datetime.datetime(2019, 5, 11, 18, 12, 43),
 datetime.datetime(2019, 5, 11, 18, 12, 41),
...]
```


https://github.com/pushshift/api for more info on parameters

