# mle_normal_distribution.py
# by Ryan Delgado June 6, 2016
# The purpose of this script is to demonstrate my knowledge of Maximum Likelihood Estimation (MLE) by first looking at
# the simple case of a normal distribution. This exercise will
# 1. Define the normal distribution and likelihood function in functions
# 2. Generate a list of random distribution of numbers with length 100
# 3. Use np.mean() and np.std() to find the mean and standard deviation of the distribution
# 4. Use MLE (via optimization) to estimate the distribution's mean and std
# 5. Verify that the parameters found using np.mean() & np.std() equal the parameters found using MLE

import numpy as np
from scipy.optimize import minimize

# Define the normal distribution
# params:
#   x - double; the observation in the sample/distribution
#   sig - double; the standard deviation of the distribution; default 1 for standard normal distribution
#   mu - double; the mean of the distribution; default 0 for standard normal distribution
def normal_dist(x, sig, mu):
    return (1 / np.sqrt(2 * (sig ** 2) * np.pi)) * np.exp((-(x - mu) ** 2) / (2 * (sig ** 2)))



# Define the likelihood function
# params:
#   x_array - 1xN ndarray; an array of the sample
def norm_log_likelihood_function(x_array, sig, mu):
     return np.log(np.prod([normal_dist(x, sig, mu) for x in x_array]))


sample = np.random.normal(5, 2, 100)

nll = lambda *args: -norm_log_likelihood_function(*args)
result = minimize(nll, [4,1], args=(sig, mu))
