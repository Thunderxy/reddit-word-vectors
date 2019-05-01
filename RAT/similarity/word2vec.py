import gensim
import logging
import multiprocessing
import numpy as np


def make_model(post_data, size_=300, window_=2, min_count_=2, epochs_=1):
    cores = multiprocessing.cpu_count()

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    model = gensim.models.Word2Vec(size=size_, window=window_, min_count=min_count_, workers=cores-1)
    model.build_vocab(post_data)
    model.train(post_data, total_examples=len(post_data), epochs=epochs_)

    return model


def cos_sim(a, b):
    a = np.squeeze(a)
    b = np.squeeze(b)

    angle = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    if np.isnan(angle):
        return 0
    else:
        return angle


# print(model.wv.similarity('', ''))

# for i in my_model.wv.most_similar(positive=[''], topn=100):
#     print(i)
