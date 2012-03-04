import numpy as np
import matplotlib.pyplot as plot
import sys

def exp(mean, samples = 100):
	y = []
	lambda_param = (1 / mean)
	for i in range(0, samples):
		rand = np.random.rand()
		y.append(np.log(1 - rand) / (-1.0 * lambda_param))

	plot.hist(y, bins = 100)
	plot.show()

def normal(mean = 0, stddev = 1, samples = 100):
	y = []
	for i in range(0, samples):
		rand1 = np.random.rand()
		rand2 = np.random.rand()
		var = np.sqrt(-2 * np.log(rand1)) * np.cos(2 * np.pi * rand2)
		y.append((var * stddev) + mean)
	plot.hist(y, bins = 100)
	plot.show()

normal(mean = 40, stddev = 1, samples = 10000)
