import numpy as np


class BernoulliNaiveBayes:
    def __init__(self, k=1):
        self.k = k


    def fit(self, X_train, y_train):
        '''
        Fits the Naive Bayes Classifier.
        :param X_train: nxd ndarray of feature vectors for each observation
        :param y_train: nx1 ndarray of labels
        '''

        # Find the label counts and probabilities
        count_y = dict(*np.unique(y_train, return_counts=True))
        self.p_y = np.matrix(list(count_y.values())) / sum(count_y.values())

        # Find the indices where X_train is nonzero; Calculate p_x for each word
        X_train_nz = (X_train != 0).astype(int)
        self.p_x = np.sum(X_train_nz, axis=0)

        # Calculate the prior matrix
        prior_vectors = []
        for label, count in count_y.items():
            y_train_islabel = np.matrix(y_train == label).astype(int)
            prior_vector = (np.matmul(y_train_islabel, X_train_nz) + self.k) / count
            prior_vectors.append(prior_vector)

        self.p_xy = np.vstack(prior_vectors)

        # Calculate the posterior matrix
        self.p_yx = np.divide(np.multiply(self.p_xy, self.p_y.T), self.p_x)


    def predict(self, X_pred):
        '''

        :param X_pred: 
        :return: 
        '''

        y_pred = []
        for i in range(X_pred.shape[0]):
            obs = X_pred[i, :]
            sum_logl = np.sum(np.log(self.p_yx[:, np.where(obs != 0)[0]]), axis=1)
            y_pred.append(sum_logl.argmax())

        return np.array(y_pred)
