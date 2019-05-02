from RAT.similarity.text_preprocessing import clean_posts, clean_text
from RAT.similarity.word2vec import make_model, cos_sim
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def post2vec(posts, model, size=300):
    post_vec_lst = []

    if isinstance(posts[0], str):
        posts = [posts]

    for post in posts:

        sum_post = np.zeros(size)

        for word in post:
            try:
                sum_post += model[word]
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

    return cosine_similarity(compare_vec, posts_vec).ravel()


def most_similar(sim_vec, post_data, n=100):

    sort_ind = sim_vec.argsort()[::-1][:n]

    for i, j in enumerate(sort_ind):
        print('{}: {}'.format(i, ' '.join(post_data[j])))


file_name = '.json.gz'
post_data = clean_posts(file_name)
my_model = make_model(post_data, size_=300, window_=2, min_count_=2, epochs_=10)

sim_nums = post_sim("", post_data, my_model)

most_similar(sim_nums, post_data)
