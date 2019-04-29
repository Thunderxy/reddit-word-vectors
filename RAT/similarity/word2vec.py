from RAT.similarity.text_preprocessing import clean_posts
import gensim
import logging
import multiprocessing


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


file_name = '.json.gz'
post_data = clean_posts(file_name)

cores = multiprocessing.cpu_count()

model = gensim.models.Word2Vec(size=300, window=2, min_count=2, workers=cores-1)
model.build_vocab(post_data)
model.train(post_data, total_examples=len(post_data), epochs=10)


# print(model.wv.similarity('', ''))

# for i in model.wv.most_similar(positive=[''], topn=100):
#     print(i)
