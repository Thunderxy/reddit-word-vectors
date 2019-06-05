from RAT.text_processing.process_reddit import clean_text
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA


def post2vec(posts, model, word_dct, size=300, a=0.001):
    post_vec_lst = []

    if isinstance(posts[0], str):
        posts = [posts]

    for post in posts:

        sum_post = np.zeros(size)

        for word in post:
            try:
                sum_post += model[word] * (a / (a + word_dct[word]))
            except KeyError:
                sum_post += np.zeros(size)

        post_vec_lst.append(sum_post)

    post_mat = np.array(post_vec_lst)

    return post_mat


def post_sim(compare_str, posts, model, word_dct):
    compare_vec = post2vec(clean_text(compare_str), model, word_dct)
    posts_vec = post2vec(posts, model, word_dct)

    sentence_set = posts_vec
    pca = PCA()
    pca.fit(np.array(sentence_set))
    u = pca.components_[0]
    u = np.multiply(u, np.transpose(u))  # u x uT

    # vs = vs -u x uT x vs
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
