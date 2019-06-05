from RAT.vector_model.word2vec_iter import MySentences, make_model, save_model, load_model


sents = MySentences(['askreddit_comments0.json.gz',
                     'askreddit_comments1.json.gz',
                     'askreddit_comments2.json.gz',
                     'askreddit_comments3.json.gz',
                     'askreddit_comments4.json.gz'])

wv_model = make_model(sents)

save_model('5days_askreddit_model.kv', wv_model)

# my_model = load_model('5days_askreddit_model.kv')

# print(my_model.similar_by_word("cat"))
#
# print(len(my_model.wv.vocab))
#
# for word in my_model.vocab:
#     print(word, ':', my_model.vocab[word].count)
