from RAT.vector_model.word2vec_iter import MySentences, make_model, save_model, load_model
import os
from pathlib import Path
from gensim.models import FastText
from gensim.models import KeyedVectors


# ft stuff https://radimrehurek.com/gensim/models/fasttext.html#usage-examples

dir_path = str(Path(os.path.abspath(__file__)).parents[1]) + '/data/reddit_data'
file_lst = os.listdir(dir_path)

# iterator stuff
reddit_data = []

for file in file_lst:
    if file[0] != 'r' and file != '.gitignore':
        reddit_data.append(file)

reddit_data_ = ['math_comments9.json.gz']

sents_iter = MySentences(reddit_data_)

# making ft
# model4 = FastText(size=4, window=3, min_count=1)
# model4.build_vocab(sentences=sents_iter)
# total_examples = model4.corpus_count
# model4.train(sentences=sents_iter, total_examples=total_examples, epochs=1)

# saving ft as model
# path_1 = str(Path(os.path.abspath(__file__)).parents[0]) + '/new_model.model'
# model4.save(path_1)

# saving to kv directly
# path_2 = str(Path(os.path.abspath(__file__)).parents[0]) + '/new_model.kv'
# word_vectors = model4.wv
# word_vectors.save(path_2)

# saving ft as kv from model
# my_model = FastText.load(path_1)
# word_vectors = my_model.wv
# word_vectors.save(path_2)

# loading kv
# word_vectors = KeyedVectors.load(path_2, mmap='r')





# w2v stuff
# wv_model = make_model(sents_iter, window_=3, min_count_=10, epochs_=1)

# save_model('test.kv', wv_model)

# my_model = load_model('5days_askreddit_model.kv')

# print(my_model.similar_by_word("cat"))
#
# print(len(my_model.wv.vocab))
#
# for word in my_model.vocab:
#     print(word, ':', my_model.vocab[word].count)


# https://radimrehurek.com/gensim/models/fasttext.html#usage-examples
# https://radimrehurek.com/gensim/models/keyedvectors.html
# https://radimrehurek.com/gensim/models/word2vec.html
