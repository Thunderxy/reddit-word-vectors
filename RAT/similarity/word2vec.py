from RAT.pushshift.get_json_data import load_posts, get_post_list
import gensim
import os
import logging
import multiprocessing


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def read_input(file_name):
    file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../pushshift/' + file_name)
    load = load_posts(file)
    return get_post_list(load)


def sentences(data):
    tokenized = []
    for title in data:
        tokenized.append(gensim.utils.simple_preprocess(title.title))

    return tokenized


file_name = ''
post_data = sentences(read_input(file_name))

cores = multiprocessing.cpu_count()

model = gensim.models.Word2Vec(size=300, window=2, min_count=2, workers=cores-1)
model.build_vocab(post_data)
model.train(post_data, total_examples=len(post_data), epochs=5)


# print(model.wv.similarity('', ''))

# for i in model.wv.most_similar(positive=[''], topn=100):
#     print(i)
