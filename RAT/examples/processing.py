from RAT.pushshift.load_data import Content
from RAT.text_processing.process_reddit import word2vec_input, count_words


my_file = Content('askreddit_comments.json.gz')
my_comments = my_file.load_comments()

# for i in my_comments:
#     sents = word2vec_input([i])
#     print(sents)

for_word2vec = word2vec_input(my_comments)

words_dct = count_words(for_word2vec)
