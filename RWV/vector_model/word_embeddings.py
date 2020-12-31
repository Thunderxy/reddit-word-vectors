import logging
import os
import multiprocessing
from pathlib import Path
from RWV.pushshift.load_data import Content
from RWV.text_processing.process_reddit import word2vec_input, doc2vec_input
from gensim.models import Word2Vec, FastText, KeyedVectors
from gensim.models.doc2vec import Doc2Vec, TaggedDocument


class SentenceIter:

    def __init__(self, file_name_lst, content, model_type):
        """ Iterator class that produces list of strings for each given sentence.

        Parameters
        ----------
        file_name_lst: list
            List of files of form .json.gz that contain reddit data.
        content: str
            'post' or 'comment'.
        model_type: str
            'word2vec', 'doc2vec' or 'fasttext'.

        Yields
        ------
        List of strings.

        documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(common_texts)]

        """
        self.file_name_lst = file_name_lst
        self.content = content
        self.model_type = model_type

    def __iter__(self):

        c = -1
        for file_name in self.file_name_lst:

            if self.content == 'post':
                saved_content = Content(file_name).load_posts()
            elif self.content == 'comment':
                saved_content = Content(file_name).load_comments()
            else:
                raise NameError

            if self.model_type == 'word2vec' or self.model_type == 'fasttext':
                for obj in saved_content:
                    sent_lst = word2vec_input([obj])
                    for sent in sent_lst:
                        yield sent
            else:
                for obj in saved_content:
                    doc = doc2vec_input([obj])
                    c += 1
                    yield TaggedDocument(doc, [c])

                c += 1


class WordEmbedding:

    def __init__(self, model_type):
        """ Class for making, saving and loading Gensim word embeddings.

        Parameters
        ----------
        model_type: str
            'word2vec', 'doc2vec' or 'fasttext'.

        Other Parameters
        ----------------
        model: wv model
            Is set by make_model, saved by save_model and loaded by load_model.

        Notes
        -----
        Save to .kv if no more training else save as .model.

        References
        ----------
        https://radimrehurek.com/gensim/models/word2vec.html
        https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html

        https://radimrehurek.com/gensim/models/doc2vec.html
        https://radimrehurek.com/gensim/auto_examples/tutorials/run_doc2vec_lee.html

        https://fasttext.cc/
        https://radimrehurek.com/gensim/models/fasttext.html
        https://radimrehurek.com/gensim/auto_examples/tutorials/run_fasttext.html

        """
        self.model_type = model_type.lower()
        self.model = None

    def make_model(self, sentences, content, log=True, size=300, window=5, min_count=10, epochs=5, workers=None, **kwargs):
        """

        Parameters
        ----------
        sentences: list of str
            List of file paths to saved reddit objects.
        content: str
            'post' or 'comment'
        log: bool
            Use Gensim's logging.
        size: int
            Vector size of model.
        window: int
            Context window size.
        min_count: int
            Ignore words with number of occurrences below this.
        epochs: int
            Times to go over data.
        workers: int
            Number of cores.
        kwargs: parameters
            See Gensim docs for more parameters to put in Word2vec or FastText.

        Notes on FastText
        -----------------
        The size of the model will increase linearly with the number of buckets. The size of the input matrix
        is DIM x (VS + BS), where VS is the number of words in the vocabulary and BS is the number of buckets.

        BS default: 2000000

        Notes
        -----
        Path to saved data: path = str(Path(os.path.abspath(__file__)).parents[1]) + '/data/reddit_data'
        Sentences and words in model: total sentences: self.model.corpus_count, total words: self.model.corpus_total_words

        Returns
        -------
        self

        """
        if log:
            logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        if not workers:
            workers = multiprocessing.cpu_count()

        sents_iter = SentenceIter(sentences, content=content, model_type=self.model_type)

        if self.model_type == 'word2vec':
            self.model = Word2Vec(size=size, window=window, min_count=min_count, workers=workers, **kwargs)
        elif self.model_type == 'fasttext':
            self.model = FastText(size=size, window=window, min_count=min_count, workers=workers, **kwargs)
        elif self.model_type == 'doc2vec':
            self.model = Doc2Vec(size=size, window=window, min_count=min_count, workers=workers, **kwargs)
        else:
            raise NameError

        self.model.build_vocab(sents_iter)

        if self.model_type == 'doc2vec':
            self.model.train(documents=sents_iter, total_examples=self.model.corpus_count, epochs=epochs)
        else:
            self.model.train(sentences=sents_iter, total_examples=self.model.corpus_count, epochs=epochs)

        return self

    def save_model(self, file_name, path=None):

        if not path:
            path = str(Path(os.path.abspath(__file__)).parents[1]) + '/data/models/' + file_name

        if file_name[-3:] == '.kv':
            keyed_model = self.model.wv
            keyed_model.save(path)
        else:
            self.model.save(path)

        return True

    def load_model(self, file_name, path=None):

        if not path:
            path = str(Path(os.path.abspath(__file__)).parents[1]) + '/data/models/' + file_name

        if file_name[-3:] == '.kv':
            self.model = KeyedVectors.load(path, mmap='r')
        else:
            if self.model_type == 'word2vec':
                self.model = Word2Vec.load(path)
            elif self.model_type == 'fasttext':
                self.model = FastText.load(path)
            elif self.model_type == 'doc2vec':
                self.model = Doc2Vec.load(path)
            else:
                raise NameError

        return self.model
