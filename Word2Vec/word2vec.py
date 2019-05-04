import logging

import numpy as np
import tensorflow as tf
# import tensorflow.contrib.eager as tfe
from keras.preprocessing.text import Tokenizer

logger = logging.getLogger('word2vec')


def batch(iterable, n=1):
    """Utility function for splitting an iterable into an iterable of smaller batches"""
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def pad_sentence(sentence, window_size=1):
    START_TOKEN = '<s> '
    END_TOKEN = ' </s>'
    padded_sentence = (START_TOKEN * window_size) + sentence + (END_TOKEN * window_size)
    return padded_sentence


def cbow_preprocess(sequence, window_size=1):
    """
    Turns 'the quick brown fox jumped over the lazy dog' into
    [[('the', 'brown'), 'quick'],
     [('quick', 'fox'), 'brown'],
     [('brown', 'jumped'), 'fox'],
     ...

     except as NumPy arrays.
    """
    inputs = []
    labels = []

    for i, token in enumerate(sequence):
        if ((i < window_size) | (i > len(sequence) - (window_size + 1))):
            pass
        else:
            previous_words = tuple(sequence[i - window_size:i])
            next_words = tuple(sequence[i + 1:i + window_size + 1])
            context = previous_words + next_words
            label = token
            inputs.append(context)
            labels.append(label)

    inputs = np.squeeze(np.array(inputs))
    labels = np.expand_dims(np.array(labels), 1)

    return inputs, labels


def skipgram_preprocess(sequence, window_size=1):
    """
    Turns 'the quick brown fox jumped over the lazy dog' into
    [('quick', 'the'),
     ('quick', 'brown'),
     ('brown', 'quick'),
     ('brown', 'fox'),
     ...

     except as NumPy arrays.
    """
    inputs = []
    labels = []

    for i, token in enumerate(sequence):
        if ((i < window_size) | (i > len(sequence) - (window_size + 1))):
            pass
        else:
            for context in sequence[i - window_size:i]:
                inputs.append(context)
                labels.append(token)
            for context in sequence[i + 1:i + window_size + 1]:
                inputs.append(context)
                labels.append(token)

    inputs = np.squeeze(np.array(inputs))
    labels = np.expand_dims(np.array(labels), 1)

    return inputs, labels

class Word2Vec:
    """
    ToDo: Write the docs.
    ToDo: Add logging statements.
    """

    def __init__(self, texts, embedding_dim=100, window_size=2, architecture='skipgram',
                 batch_size=32, num_epochs=1, num_sampled=200):

        self.embedding_dim = embedding_dim
        self.window_size = window_size
        self.batch_size = batch_size
        self.num_epochs = num_epochs
        self.num_sampled = num_sampled
        self.padded_texts = [pad_sentence(text, window_size) for text in texts]

        self.tokenizer = Tokenizer()
        self.tokenizer.fit_on_texts(self.padded_texts)
        self.tokenized_texts = self.tokenizer.texts_to_sequences(self.padded_texts)
        self.vocab_size = len(self.tokenizer.word_index)

        self._initialize_tensors()

        self.embedding_matrix_numpy = None
        self.embedding_dict = None

        if architecture == 'cbow':
            self.train_op = self._get_skipgram_train_op()
            self.preprocessor = cbow_preprocess
        else:
            self.train_op = self._get_cbow_train_op()
            self.preprocessor = skipgram_preprocess

    def _initialize_tensors(self):
        shape = (self.vocab_size, self.embedding_dim)
        self.embedding_matrix_ = tf.get_variable(name='embedding_matrix',
                                                 initializer=tf.random_uniform(shape, -1.0, 1.0))
        self.nce_weights_ = tf.get_variable(name='nce_weights',
                                            initializer=tf.truncated_normal(shape, stddev=1.0 / (self.vocab_size ** 0.5)))
        self.nce_biases_ = tf.get_variable(name='nce_biases',
                                           initializer=tf.zeros([self.vocab_size]))
        self.train_inputs_ = tf.placeholder(tf.int32, shape=[self.batch_size])
        self.train_labels_ = tf.placeholder(tf.int32, shape=[self.batch_size, 1])

    def _concat_train_data(self, preprocessed_texts):
        if self.preprocessor == skipgram_preprocess:
            contexts = np.hstack(t[0] for t in preprocessed_texts)
        else:
            contexts = np.vstack(t[0] for t in preprocessed_texts)
        labels = np.vstack(t[1] for t in preprocessed_texts)

        return contexts, labels

    def _get_skipgram_train_op(self):
        """Graph for the skipgram Word2Vec model."""

        embeddings_ = tf.nn.embedding_lookup(self.embedding_matrix_, self.train_inputs_)
        loss = tf.reduce_mean(
            tf.nn.nce_loss(
                weights=self.nce_weights_,
                biases=self.nce_biases_,
                labels=self.train_labels_,
                inputs=embeddings_,
                num_sampled=self.num_sampled,
                num_classes=self.vocab_size
            )
        )
        train_op = tf.train.GradientDescentOptimizer(learning_rate=1.0).minimize(loss)

        return train_op

    def _get_cbow_train_op(self):
        """Graph for the cbow Word2Vec model."""

        embeddings_ = tf.nn.embedding_lookup(self.embedding_matrix_, self.train_inputs_)
        bow = tf.reduce_sum(embeddings_, axis=1)
        loss = tf.reduce_mean(
            tf.nn.nce_loss(
                weights=self.nce_weights_,
                biases=self.nce_biases_,
                labels=self.train_labels_,
                inputs=embeddings_,
                num_sampled=self.num_sampled,
                num_classes=self.vocab_size
            )
        )
        train_op = tf.train.GradientDescentOptimizer(learning_rate=1.0).minimize(loss)

        return train_op

    def train(self, new_text=None):
        """Trains the Word2Vec embeddings."""

        # ToDo: Handle new_text
        # Ensure that a list of sentences still results in the expected
        # output.
        preprocessed_texts = [self.preprocessor(text) for text in self.tokenized_texts]
        train_inputs, train_labels = self._concat_train_data(preprocessed_texts)

        with tf.Session() as sess:
            for i in range(self.num_epochs):
                for inputs, labels in batch(zip(train_inputs, train_labels), self.batch_size):
                    feed_dict = {
                        self.train_inputs_: inputs,
                        self.train_labels_: labels
                    }
                    _ = sess.run(self.train_op, feed_dict=feed_dict)

        logger.info('Training finished.')
        self.embedding_matrix_numpy = sess.eval(self.embedding_matrix_)

    def _build_embedding_dict(self):
        word_to_id = self.tokenizer.word_index
        id_to_word = dict(zip(word_to_id.values(), word_to_id.keys()))

        embedding_dict = {}
        for i in range(self.embedding_matrix_numpy.shape[0]):
            word = id_to_word[i]
            embedding_dict[word] = self.embedding_matrix_numpy[i, :]

        return embedding_dict

    @property
    def embeddings(self):
        if not self.embedding_dict:
            self.embedding_dict = self._build_embedding_dict()

        return self.embedding_dict