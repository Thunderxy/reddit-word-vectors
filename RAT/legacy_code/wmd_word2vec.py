# https://markroxor.github.io/gensim/static/notebooks/WM

from gensim.similarities import WmdSimilarity
from RAT.legacy_code.word2vec import load_model
from RAT.text_processing.process_reddit import clean_text
from RAT.pushshift.get_data import fPosts
from RAT.text_processing.process_reddit import unpickle_this
import time

my_file = fPosts('')
Posts = my_file.get_content_list(my_file.load_posts())

my_model = load_model('')

my_model.init_sims(replace=True)

# s1 = clean_text('')
# s2 = clean_text('')
# distance = my_model.wmdistance(s1, s2)

post_data = unpickle_this('')

instance = WmdSimilarity(post_data, my_model, num_best=10)

query = clean_text('')

start = time.time()
sims = instance[query]
print('t={} s\n'.format(time.time() - start))


for i in range(10):
    print('sim = {}'.format(sims[i][1]))
    print('post: {}\n'.format(Posts[sims[i][0]].title))
