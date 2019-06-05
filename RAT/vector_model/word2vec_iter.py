# https://rare-technologies.com/word2vec-tutorial/
# https://radimrehurek.com/gensim/models/word2vec.html#gensim.models.word2vec.Word2Vec
# https://radimrehurek.com/gensim/models/keyedvectors.html#gensim.models.keyedvectors.WordEmbeddingsKeyedVectors

from gensim.models import Word2Vec, KeyedVectors
from gensim.test.utils import get_tmpfile
import logging
import os
import multiprocessing
from RAT.pushshift.load_data import Content
from RAT.text_processing.process_reddit import word2vec_input


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class MySentences:

    def __init__(self, file_name_lst):
        self.file_name_lst = file_name_lst

    def __iter__(self):
        for file_name in self.file_name_lst:
            obj_content = self.preprocess(file_name)
            for obj in obj_content:
                sent_lst = word2vec_input([obj])
                for sent in sent_lst:
                    yield sent

    @staticmethod
    def preprocess(file_name):
        file_content = Content(file_name)

        if 'comments' in file_name:
            obj_content = file_content.load_comments()
        elif 'posts' in file_name:
            obj_content = file_content.load_posts()
        else:
            raise ValueError('no posts/comments in file name')

        return obj_content


def make_model(sentences, size_=300, window_=2, min_count_=10, epochs_=5):
    """ Gensim word2vec.

    Args:
        sentences: sentence iterator class
        size_: vector size
        window_: distance from left and right
        min_count_: minimal word count (discards words that smaller then min_count_
        epochs_: times to go over data

    Returns:
        word2vec model

    """
    cores = multiprocessing.cpu_count()

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    model = Word2Vec(size=size_, window=window_, min_count=min_count_, workers=cores-1)
    model.build_vocab(sentences)
    model.train(sentences, total_examples=model.corpus_count, epochs=epochs_)

    return model


def save_model(file_name, model):
    """Save to .kv if no more training"""

    path = get_tmpfile(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/models/' + file_name))

    if file_name[-3:] == '.kv':
        keyed_model = model.wv
        keyed_model.save(path)
    else:
        model.save(path)


def load_model(file_name):
    path = get_tmpfile(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/models/' + file_name))

    if file_name[-3:] == '.kv':
        return KeyedVectors.load(path, mmap='r')
    else:
        return Word2Vec.load(path)
