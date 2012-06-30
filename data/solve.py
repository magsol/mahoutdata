import matplotlib.pyplot as plot
import numpy as np
import scipy.linalg
import sklearn.cluster
import sys

COLORS = ['ro', 'b^', 'gs', 'yo', 'm^', 'ks']

def usage():
	'''
	How to use this program.
	'''
	print '$> python solve.py <raw input file> <csv affinity file> <k>'
	print '\t<RAW>\t\tPath to the raw data input file'
	print '\t<CSV>\t\tPath to CSV-format affinity file'
	print '\tK <#>\t\tK in spectral k-means'

def main(raw, aff, k):
	'''
	Kicks off the main solver.

	Parameters
	----------
	raw : string
		Path to the input file containing the raw data.
	aff : string
		Path to the input file containing the CSV affinities.
	k : integer
		K in spectral k-means.

	Returns
	-------
	None
	'''
	# Load the affinity matrix and construct the normalized Laplacian.
	A = np.loadtxt(aff, delimiter = ',')
	D = np.zeros(shape = A.shape)
	for i in range(0, np.size(D, axis = 0)):
		D[i, i] = 1.0 / np.sqrt(np.sum(A[i, :]))
	L = np.dot(np.dot(D, A), D)

	# Perform the eigen-decomposition. Eigenvalues and corresponding 
	# eigenvectors are sorted from smallest to largest, but only the k
	# largest are taken, so no need to reverse their order.
	M = np.size(L, axis = 0)
	eigvals, Y = scipy.linalg.eigh(L, eigvals = (M - 1 - k, M - 1))

	# Perform K-means clustering on our embedded dataset Y.
	kmeans = sklearn.cluster.KMeans(k = k)
	labels = kmeans.fit_predict(Y)
	rawdata = np.loadtxt(raw, delimiter = ',')
	for i in range(0, np.size(rawdata, axis = 0)):
		plot.plot(rawdata[i, 0], rawdata[i, 1], COLORS[labels[i]])
	plot.show()

if __name__ == '__main__':
	if len(sys.argv) != 4:
		usage()
		quit()
	main(sys.argv[1], sys.argv[2], int(sys.argv[3]))