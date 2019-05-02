# smooth inverese frequency
# https://stackoverflow.com/questions/22129943/how-to-calculate-the-sentence-similarity-using-word2vec-model-of-gensim-with-pyt
# https://github.com/PrincetonML/SIF
# https://github.com/peter3125/sentence2vec/blob/master/sentence2vec.py
# TODO: make this thing

from RAT.similarity.text_preprocessing import clean_posts, clean_text, count_words
from RAT.similarity.word2vec import make_model
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA


def get_freq(posts):
    return count_words(posts)


def post2vec(posts, model, size=300):
    post_vec_lst = []

    word_dct = get_freq(posts)

    if isinstance(posts[0], str):
        posts = [posts]

    for post in posts:

        sum_post = np.zeros(size)

        for word in post:
            try:
                sum_post += model[word] * (1 / (1 + word_dct[word]))
            except KeyError:
                sum_post += np.zeros(size)

        if np.count_nonzero(sum_post) == 0:
            sum_post += 1e-6

        post_vec_lst.append(sum_post)

    post_mat = np.array(post_vec_lst)

    return post_mat


def post_sim(compare_str, posts, model):
    compare_vec = post2vec(clean_text(compare_str), model)
    posts_vec = post2vec(posts, model)

    sentence_set = posts_vec

    pca = PCA()
    pca.fit(np.array(sentence_set))
    u = pca.components_[0]  # the PCA vector
    u = np.multiply(u, np.transpose(u))  # u x uT

    # resulting sentence vectors, vs = vs -u x uT x vs
    sentence_vecs = []
    for vs in sentence_set:
        sub = np.multiply(u, vs)
        sentence_vecs.append(np.subtract(vs, sub))

    sentence_mat = np.array(sentence_vecs)

    return cosine_similarity(compare_vec, sentence_mat).ravel()


def most_similar(sim_vec, post_data, n=100):

    sort_ind = sim_vec.argsort()[::-1][:n]

    for i, j in enumerate(sort_ind):
        print('{}: {}'.format(i, ' '.join(post_data[j])))


file_name = '.json.gz'
post_data = clean_posts(file_name)
my_model = make_model(post_data, size_=300, window_=2, min_count_=2, epochs_=10)

sim_nums = post_sim("", post_data, my_model)

most_similar(sim_nums, post_data)
