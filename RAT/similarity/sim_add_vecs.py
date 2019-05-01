from RAT.similarity.text_preprocessing import clean_posts, clean_text
from RAT.similarity.word2vec import make_model, cos_sim
import numpy as np
import heapq


def post2vec(posts, model, size=300):
    post_vec_lst = []

    if isinstance(posts[0], str):
        posts = [posts]

    for post in posts:

        sum_post = np.zeros(shape=(1, size))

        for word in post:
            try:
                sum_post += model[word]
            except KeyError:
                sum_post += np.zeros(shape=(1, size))

        if np.count_nonzero(sum_post) == 0:
            sum_post += 1e-6

        post_vec_lst.append(sum_post)

    return post_vec_lst


def post_sim(compare_str, posts, model):
    compare_vec = post2vec(clean_text(compare_str), model)
    posts_vec = post2vec(posts, model)

    sim_lst = []

    for post_vec in posts_vec:
        sim_lst.append(cos_sim(compare_vec, post_vec))

    return sim_lst


def most_similar(sim_lst, post_data, n=100):
    top_nums = heapq.nlargest(n, sim_lst)

    for count, num in enumerate(top_nums):
        ind = sim_lst.index(num)
        s = ' '.join(post_data[ind])

        print('{}: | cos = {:0.2f} | {}'.format(count, num, s))


file_name = '.json.gz'
post_data = clean_posts(file_name)
my_model = make_model(post_data, size_=300, window_=2, min_count_=2, epochs_=10)

sim_nums = post_sim("", post_data, my_model)

most_similar(sim_nums, post_data)
