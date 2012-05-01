import numpy as np
import sys

def compute_distances(points):
	'''
	Computes the pairwise euclidean distances for all points.
	This allows us to do some useful stuff, like figure out what
	the median distance is for calculating affinities.
	'''
	numpoints = np.size(points, axis = 0)
	distances = np.zeros(shape = (numpoints, numpoints))
	for i in range(0, numpoints):
		for j in range(i + 1, numpoints):
			distances[i, j] = np.linalg.norm(points[i] - points[j])
	return distances

def compute_affinity(distance, sigma, threshold):
	'''
	Computes the gaussian affinity between x and y, using the threshold
	value to determine if the calculation is even needed, or if the 
	affinity is 0. If the distance is within the threshold, we use
	the radial basis kernel for calculating affinity.
	'''
	if distance > threshold:
		return 0.0
	else:
		return np.exp(-(distance ** 2) / (2 * (sigma ** 2)))


if len(sys.argv) != 4:
	print '$> python affinity.py <rawdata> <neighborhood> <output>\n'
	print '\trawdata\t\tRaw input data file'
	print '\tneighborhood\tDistance threshold for calculating pointwise affinity'
	print '\toutput\tOutput file for the affinity matrix (in Mahout SKM format)'
	quit()

rawdata = np.loadtxt(sys.argv[1], delimiter = ',')
neighborhood = float(sys.argv[2])
output = sys.argv[3]
points = np.size(rawdata, axis = 0)
distances = compute_distances(rawdata)
sigma = np.std(distances.flatten())

f = open(output, 'w')
# Compute pair-wise affinities.
for i in range(0, points):
	for j in range(i, points):
		affinity = compute_affinity(distances[i, j], sigma, neighborhood)
		if i == j:
			affinity = 0.0
		f.write('%s,%s,%s\n' % (i, j, affinity))
f.close()