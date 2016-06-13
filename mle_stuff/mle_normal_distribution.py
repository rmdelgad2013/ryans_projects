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
#   params - list: contains the mean and std deviation params for the normal distribution
#   x - NumPy array: contains the observations for the random variable X
def normal_dist(params, x):
    sig, mu = params
    return (1 / np.sqrt(2 * (sig ** 2) * np.pi)) * np.exp((-(x - mu) ** 2) / (2 * (sig ** 2)))



# Define the likelihood function
# params:
#   x_array - 1xN ndarray; an array of the sample
def norm_log_likelihood_function(params, x_array):
     return np.log(np.prod([normal_dist(params, x) for x in x_array]))





nll = lambda *args: -norm_log_likelihood_function(*args)

sample = np.random.normal(5, 4, 100)
result = minimize(nll, [4,1], args=(sample))
print(result["x"])
