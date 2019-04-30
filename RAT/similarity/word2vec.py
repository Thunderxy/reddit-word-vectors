from RAT.similarity.text_preprocessing import clean_posts, clean_text
import gensim
import logging
import multiprocessing
import numpy as np
import heapq


def make_model(post_data):
    cores = multiprocessing.cpu_count()

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    model = gensim.models.Word2Vec(size=300, window=2, min_count=2, workers=cores-1)
    model.build_vocab(post_data)
    model.train(post_data, total_examples=len(post_data), epochs=10)

    return model


def cos_sim(a, b):
    a = np.squeeze(a)
    b = np.squeeze(b)

    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    angle = dot_product / (norm_a * norm_b)

    if np.isnan(angle):
        return 0
    else:
        return angle


def text_sim(compare, posts, model):
    clean_sentence = clean_text(compare)
    cos_sim_lst = []

    sum_sentence = np.zeros(shape=(1, 300))
    for word in clean_sentence:
        try:
            sum_sentence += model[word]
        except KeyError:
            sum_sentence += np.zeros(shape=(1, 300))

    for post in posts:
        sum_post = np.zeros(shape=(1, 300))

        for word in post:
            try:
                sum_post += model[word]
            except KeyError:
                sum_post += np.zeros(shape=(1, 300))

        cos_sim_lst.append(cos_sim(sum_sentence, sum_post))

    return cos_sim_lst


file_name = '.json.gz'
post_data = clean_posts(file_name)
my_model = make_model(post_data)


nums = text_sim("", post_data, my_model)

largest_nums = heapq.nlargest(100, nums)

x = 0
for i in largest_nums:

    j = nums.index(i)
    s = ' '.join(post_data[j])
    x += 1

    print('{}: | cos = {:0.2f} | {}'.format(x, i, s))


# print(model.wv.similarity('', ''))

# for i in my_model.wv.most_similar(positive=[''], topn=100):
#     print(i)
