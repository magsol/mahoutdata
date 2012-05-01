import sys
import numpy as np
import util

'''
This script generates n-dimensional clusters of data by
sampling from gaussian distributions. This can be useful
for both classic and more specialized clustering algorithms
for comparing their respective performances.
'''

def too_close(point, points, threshold):
	'''
	Determines whether or not "point" is too close to any of the values
	in "points", using the euclidean norm and the threshold.
	'''
	for value in points:
		if np.linalg.norm(point - value) < threshold:
			return True
	return False

#
# Here's where the script actually goes to work.
#
clusters, \
points, \
output, \
separation, \
maximum, \
dimensions, \
minvar, \
maxvar = util.read_args(sys.argv, 'gaussian')

# Generate the centroids.
centroids = []
data = []
for i in range(0, clusters):
	centroid = np.random.uniform(-maximum, maximum, dimensions)
	while (too_close(centroid, centroids, separation)):
		centroid = np.random.uniform(-maximum, maximum, dimensions)
	centroids.append(centroid)

	# Generate the points in each centroid.
	variance = np.random.uniform(minvar, maxvar)
	for j in range(0, points):
		data.append(np.random.normal(centroid, variance))

# Write out the data.
data = np.array(data)
np.savetxt(output, data, fmt = '%s', delimiter = ',')