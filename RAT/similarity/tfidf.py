from RAT.pushshift.get_data import Posts
import numpy as np
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def to_angle(vec):
    lst = []
    for i in np.nditer(vec):
        try:
            lst.append(math.degrees(math.acos(i)))
        except ValueError:
            lst.append(0.0)

    return lst


post_data = Posts(n=5, size=1000, sub='TheLastAirbender').get_post_list()

train_set = ['zuko iroh azula ozai ursa']

test_set = [i.title for i in post_data]


vectorizer = CountVectorizer(stop_words='english')    # Convert a collection of text documents to a matrix of token counts

train_vec = vectorizer.fit_transform(train_set)     # Learn the vocabulary dictionary and return term-document matrix.

print(vectorizer.vocabulary_)
print(train_vec.toarray())


tf_matrix = vectorizer.transform(test_set)     # Transform documents to document-term matrix

sim = cosine_similarity(train_vec, tf_matrix)


def get_index(n, vec):
    # https://stackoverflow.com/questions/6910641/how-do-i-get-indices-of-n-maximum-values-in-a-numpy-array
    vec = vec.ravel()
    index = np.argpartition(vec, -n)[-n:]
    return index[np.argsort(vec[index])][::-1].tolist()


def index_to_post(test_set, index_lst):
    for i in index_lst:
        print(to_angle(sim.item(i))[0], test_set[i])


index_to_post(test_set, get_index(15, sim))




# smeti:
# print('--------------------')
# # tf-idf (term frequency - inverse document frequency)
# # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html
#
# tfidf = TfidfTransformer(norm='l2', smooth_idf=True)
# tfidf.fit(tf_matrix)    # Learn the idf vector
#
# tfidf_matrix = tfidf.transform(tf_matrix)   # Transform a count matrix to a tf or tf-idf representation
#
# print(tfidf_matrix.toarray())





# http://blog.christianperone.com/2013/09/machine-learning-cosine-similarity-for-vector-space-models-part-iii/
#
#
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import math
# import numpy as np
#
#
# documents = [
#             'HIDDEN DETAIL - The guy who sells the cabbages in Avatar The Last Airbender and always loses them, is the same guy who sets up the cabbage corp in Legend Of Korra.',
#             'HIDDEN DETAIL - The guy who chases down Aang and the group in Avatar The Last Airbender is the same person who joins the team later on and teaches Aang firebending! Mind Blown!!',
#             ]
#
#
# tfidf_vectorizer = TfidfVectorizer(stop_words='english', smooth_idf=True)
# tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
# print(tfidf_vectorizer.get_feature_names())
# # print(tfidf_matrix.toarray())
# # print(tfidf_matrix.shape)
#
# sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
#
# lst = []
# for i in np.nditer(sim):
#     try:
#         lst.append(math.degrees(math.acos(i)))
#     except ValueError:
#         lst.append(0.0)
#
# print(sim)
# print(lst)
#
