import operator
import re
import pickle
import os
from nltk import sent_tokenize


def remove_punctuation(sent):
    punct = r'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' + '’`”“'
    text_nopunct = ''.join(char for char in sent if char not in punct)
    return text_nopunct


def replace_numbers(sent):
    text_nonum = re.sub(r'[0-9]+', 'stevilka', sent)
    return text_nonum


def tokenization(content):
    tokens = re.split(r'\W+', content)
    tokens_no_empty = [word.lower() for word in tokens if word != '']
    return tokens_no_empty


def remove_stopword(tokenized_lst):
    nltk_stopwords = ['im'] + ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'youre', 'youve', 'youll', 'youd', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'shes', 'her', 'hers', 'herself', 'it', 'its', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'thatll', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'dont', 'should', 'shouldve', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'arent', 'couldn', 'couldnt', 'didn', 'didnt', 'doesn', 'doesnt', 'hadn', 'hadnt', 'hasn', 'hasnt', 'haven', 'havent', 'isn', 'isnt', 'ma', 'mightn', 'mightnt', 'mustn', 'mustnt', 'needn', 'neednt', 'shan', 'shant', 'shouldn', 'shouldnt', 'wasn', 'wasnt', 'weren', 'werent', 'won', 'wont', 'wouldn', 'wouldnt']
    no_stopwords = [word for word in tokenized_lst if word not in nltk_stopwords]
    return no_stopwords


# broken
# def clean_content(content):
#     """
#
#     Args:
#         content: [[sentence1], [sentence2], ..., [sentenceN]]
#
#     Returns:
#
#     """
#     cleaned = []
#
#     for i in content:
#         # words = remove_stopword(tokenization(remove_punctuation(i.title)))
#
#         words = tokenization(remove_punctuation(i.title))
#         cleaned.append(words)
#
#     return cleaned
#
#
# def clean_text(text):
#     # words = remove_stopword(tokenization(remove_punctuation(text)))
#     words = tokenization(remove_punctuation(text))
#
#     return words


def count_words(tokenized_lst, sort=None):
    word_count = {}

    for word_lst in tokenized_lst:
        for word in word_lst:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 0

    if sort:
        return sorted(word_count.items(), key=operator.itemgetter(1))
    else:
        return word_count


def pickle_this(data, file_name):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/' + file_name)

    with open(path, 'wb') as f:
        pickle.dump(data, f)


def unpickle_this(file_name):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/' + file_name)

    with open(path, 'rb') as f:
        data = pickle.load(f)

    return data


def get_sentences(content):
    """ Tokenizes posts/comments, removes punctuation, lowers strings

    Args:
        content: list of post/comment objects
        post.title: str, comment.body: str

    Returns: sentences in list [[sent1], [sent2], ...]

    """
    text_in_sent = []

    for obj in content:

        if obj.is_post:
            tokenizer = obj.title
        else:
            tokenizer = obj.body

        for sent in sent_tokenize(tokenizer):
            # a = [remove_punctuation(sent).replace('\n', ' ')]
            # b = [i.lower() for i in [remove_punctuation(sent).replace('\n', ' ')]]
            # text.append(b)
            text_in_sent.append([i.lower() for i in [replace_numbers(remove_punctuation(sent)).rstrip().replace('\n', ' ')]])

    return text_in_sent


# ex = ['I am a Dr. bot from U.S.A.. I am god at botting:). Have you ever talked to a bot?', 'beep boop. boop beep. i am a bot', 'hello there. fellow human. human fellow']

# sp = get_sentences(ex)

# print(sp)
