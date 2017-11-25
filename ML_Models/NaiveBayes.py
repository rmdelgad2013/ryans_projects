import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix


class BernoulliNaiveBayes:
    def __init__(self):
        pass

    def _calc_p_yx(self, feat, label):
        num_nonzero_x = np.sum(self.X_train[:,feat])
        p_x = num_nonzero_x / len(self.X_train[:,feat])

        num_xy = np.sum(np.where((self.X_train[:,feat] != 0) & (self.y_train == label)))
        p_xy   = num_xy / self.count_y[label]
        p_yx   = (p_xy * self.p_y[label]) / p_x

        return p_yx

    def fit(self, X_train, y_train):
        '''
        Fits the Naive Bayes Classifier.
        :param X_train: nxd ndarray of feature vectors for each observation
        :param y_train: nx1 ndarray of labels
        '''

        # Calculate P(y_i) for each label. Store in a dictionary. P(y_i) = count(y_i)/len(y_train).

        self.X_train = X_train
        self.y_train = y_train
        counts, labels = np.unique(self.y_train, return_counts=True)
        self.count_y = dict(zip(labels, counts))
        self.p_y = dict(zip(list(labels), list(counts / len(y_train))))

        # Calculate P(y|x) for each combination of x and y
        self.p_yx = {(feat, label) : self._calc_p_yx(feat, label)
                                for feat in range(X_train.shape[1])
                                for label in labels}

    def predict(self, X_pred):
        '''
        
        :param X_pred: 
        :return: 
        '''

        pass