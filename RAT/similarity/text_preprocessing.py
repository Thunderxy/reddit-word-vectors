from RAT.pushshift.file_processing import load_posts, get_post_list
import os
import operator
import re


def json_as_obj_lst(file_name):
    """Converts json to list of Post objects."""
    file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../pushshift/' + file_name)
    load = load_posts(file)
    return get_post_list(load)


def remove_punctuation(text):
    punct = r'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    text_nopunct = ''.join(char for char in text if char not in punct)
    return text_nopunct


def tokenization(text):
    tokens = re.split(r'\W+', text)
    tokens_no_empty = [word.lower() for word in tokens if word != '']
    return tokens_no_empty


def remove_stopword(tokenized_lst):
    nltk_stopwords = ['im'] + ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'youre', 'youve', 'youll', 'youd', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'shes', 'her', 'hers', 'herself', 'it', 'its', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'thatll', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'dont', 'should', 'shouldve', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'arent', 'couldn', 'couldnt', 'didn', 'didnt', 'doesn', 'doesnt', 'hadn', 'hadnt', 'hasn', 'hasnt', 'haven', 'havent', 'isn', 'isnt', 'ma', 'mightn', 'mightnt', 'mustn', 'mustnt', 'needn', 'neednt', 'shan', 'shant', 'shouldn', 'shouldnt', 'wasn', 'wasnt', 'weren', 'werent', 'won', 'wont', 'wouldn', 'wouldnt']
    no_stopwords = [word for word in tokenized_lst if word not in nltk_stopwords]
    return no_stopwords


def clean_posts(file_name):
    posts = json_as_obj_lst(file_name)
    clean_text = []

    for i in posts:
        # words = remove_stopword(tokenization(remove_punctuation(i.title)))
        words = tokenization(remove_punctuation(i.title))
        clean_text.append(words)

    return clean_text


def count_words(tokenized_lst):
    word_count = {}

    for word_lst in tokenized_lst:
        for word in word_lst:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 0

    sorted_pairs = sorted(word_count.items(), key=operator.itemgetter(1))

    return sorted_pairs


# post = clean_posts('.json')
