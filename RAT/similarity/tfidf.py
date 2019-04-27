from RAT.pushshift.get_json_data import load_posts, get_post_list
from RAT.pushshift.get_data import from_timestamp
import numpy as np
import math
import os.path
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity


def tf_sim(train_set, test_set):
    vectorizer = CountVectorizer(stop_words='english')    # Convert a collection of text documents to a matrix of token counts
    train_vec = vectorizer.fit_transform(train_set)       # Learn the vocabulary dictionary and return term-document matrix.

    print(vectorizer.vocabulary_)

    tf_matrix = vectorizer.transform(test_set)            # Transform documents to document-term matrix

    sim = cosine_similarity(train_vec, tf_matrix)

    return sim


def tfidf_sim(train_set, test_set):
    vectorizer = CountVectorizer(stop_words='english')
    train_vec = vectorizer.fit_transform(train_set)

    print(vectorizer.vocabulary_)

    tf_matrix = vectorizer.transform(test_set)            # Transform documents to document-term matrix
    tfidf = TfidfTransformer(norm='l2', smooth_idf=True)
    tfidf.fit(tf_matrix)                                  # Learn the idf vector

    tfidf_matrix = tfidf.transform(tf_matrix)             # Transform a count matrix to a tf or tf-idf representation

    sim = cosine_similarity(train_vec, tfidf_matrix)

    return sim


def get_matches(n, test_set, vec):
    vec = vec.ravel()
    index = np.argpartition(vec, -n)[-n:]
    sorted_index_list = index[np.argsort(vec[index])][::-1].tolist()

    for i in sorted_index_list:
        print('{:0.2f} - {}'.format(to_angle(vec.item(i))[0], test_set[i]))

    return sorted_index_list


def to_angle(vec):
    lst = []
    for i in np.nditer(vec):
        try:
            lst.append(math.degrees(math.acos(i)))
        except ValueError:
            lst.append(0.0)

    return lst


file_name = 'atla_all.json'
file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../pushshift/' + file_name)
load_posts = load_posts(file)
post_data = get_post_list(load_posts)

test_set = [i.title for i in post_data]
train_set = ['What happened to Aang (more specifically Raava) when Azula shot him with lightning?']


# sim_vec_tf = tf_sim(train_set, test_set)
# i_lst = get_matches(10, test_set, sim_vec_tf)
#
# for i in i_lst:
#     print(from_timestamp(post_data[i].created_utc), post_data[i].post_id)
#
# print('@@@@@@')
#
# sim_vec_tfidf = tfidf_sim(train_set, test_set)
# get_matches(10, test_set, sim_vec_tfidf)
