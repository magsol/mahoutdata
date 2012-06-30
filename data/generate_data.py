import getopt
import numpy as np
import sklearn.metrics.pairwise
import sys

def usage():
	'''
	Defines the command line parameters for using this script
	to generate toy data for clustering.
	'''
	print '$> python generate_data.py [args]'
	print '\nAll parameters are optional (defaults in brackets)'
	print '\t-t <g | r>\tWhether the data are radial or gaussian [g]'
	print '\t-c <#>\t\tNumber of clusters from which to generate points [3]'
	print '\t-p <#>\t\tNumber of points per cluster [100]'
	print '\t-d <#>\t\tDimensionality of the data [2]'
	print '\t-s <#>\t\tMinimum separation (euclidean norm) between cluster centroids [3]'
	print '\t-m <#>\t\tAbsolute maximum value for any generated data point [10]'
	print '\t-n <#>\t\tNeighborhood cut-off distance in computing affinities [2]'
	print '\t--out-raw <file>\tFilename for the output of the raw data [raw_data.txt]'
	print '\t--out-aff-csv <file>\tFilename for the output of the affinities [aff_csv_data.txt]'
	print '\t--out-aff-mahout <file>\tFilename for affinity output in Mahout format [aff_mahout_data.txt]'
	print '\t--min-var <#>\tMinimum intra-cluster variance [0.5]'
	print '\t--max-var <#>\tMaximum intra-cluster variance [1.0]'
	print '\t--sigma <#>\tSigma for the RBF kernel in computing affinities [1.0]'
	print '\t-h\t\tPrint this help!'

def read_args(args):
	'''
	Reads and processes the command-line arguments.

	Parameters
	----------
	args : List of arguments received from the command line.

	Returns
	-------
	the_type : string
		'g' or 'r', the former indicating Gaussian data, the latter indicating Radial
	clusters : integer
		Number of clusters from which to generate data.
	points_per_cluster : integer
		Number of data points per cluster.
	dimensions : integer
		Dimensionality of each data point.
	separation : float
		Minimum L2 norm distance between cluster centroids.
	abs_max : float
		Absolute maximum value for any point generated.
	neighborhood : float
		L2 distance threshold for computing pairwise affinities.
	output_raw : string
		Filename output for the raw data in CSV row vector format.
	output_aff_csv : string
		Filename output for the affinity data in CSV row vector format.
	output_aff_mahout : string
		Filename output for the affinity data in (i, j, value) format.
	min_var : float
		Minimum intra-cluster variance (controls spread of points from centroid).
	max_var : float
		Maximum intra-cluster variance (controls spread of points from centroid).
	sigma : float
		Sigma value used in computing the RBF kernel of the affinities.
	'''

	# HERE ARE THE DEFAULT VALUES FOR EACH COMMAND LINE ARGUMENT
	the_type = 'g'
	clusters = 3
	points_per_cluster = 100
	dimensions = 2
	neighborhood = 2
	output_raw = 'raw_data.txt'
	output_aff_csv = 'aff_csv_data.txt'
	output_aff_mahout = 'aff_mahout_data.txt'
	separation = 3
	abs_max = 10
	min_var = 0.5
	max_var = 1
	sigma = 1
	
	try:
		optlist, args = getopt.getopt(args[1:], 'hc:p:s:d:m:o:t:n:', \
			['max-var=', 'min-var=', 'out-raw=', 'out-aff-csv=', 'out-aff-mahout=', 'sigma='])
	except getopt.GetoptError, err:
		print str(err)
		usage()
		quit()

	for key, val in optlist:
		if key == '-c':
			clusters = int(val)
		elif key == '-t':
			the_type = val
		elif key == '-p':
			points_per_cluster = int(val)
		elif key == '-o':
			output = val
		elif key == '-s':
			separation = float(val)
		elif key == '-d':
			dimensions = int(val)
		elif key == '-m':
			abs_max = float(val)
		elif key == '-n':
			neighborhood = float(val)
		elif key == '--out-raw':
			output_raw = val
		elif key == '--out-aff-csv':
			output_aff_csv = val
		elif key == '--out-aff-mahout':
			output_aff_mahout = val
		elif key == '--min-var':
			min_var = float(val)
		elif key == '--max-var':
			max_var = float(val)
		elif key == '--sigma':
			sigma = float(val)
		elif key == '-h':
			usage()
			quit()
	return [the_type, clusters, points_per_cluster, dimensions, separation, abs_max, \
			neighborhood, output_raw, output_aff_csv, output_aff_mahout, min_var, max_var, sigma]

def too_close(the_type, point, points, threshold):
	'''
	Checks if the specified point is outside the threshold for all other points.

	Parameters
	----------
	the_type : string
		'g' for Gaussian data, 'r' for Radial data.
	point : array-like
		Scalar or n-dimensional point to compare to all others.
	points : array, shape (M,)
		List of n-dimensional points.
	threshold : float
		Threshold value for distance (L2 for Gaussian, L1 for Radial).

	Returns
	-------
	boolean
		True if point falls within the threshold, false otherwise.
	'''
	for value in points:
		to_compare = None
		if the_type == 'g':
			to_compare = np.linalg.norm(point - value)
		else:
			to_compare = np.abs(point - value)
		if to_compare < threshold:
			return True
	return False

def create_centroids(the_type, clusters, dims, separation, maxval):
	'''
	Creates a list of cluster centroids.

	Parameters
	----------
	the_type : string
		'g' or 'r' for Gaussian or radial.
	clusters : integer
		Number of clusters.
	dims : integer
		Dimensionality of the data.
	separation : float
		Minimum L2 distance between centroids.
	maxval : float
		Maximum absolute value for any point generated.

	Returns
	-------
	centroids : array, shape (clusters,)
		List of dims-dimensional cluster centroids.
	'''
	centroids = []
	for i in range(0, clusters):
		if the_type == 'g':
			centroid = np.random.uniform(-maxval, maxval, dims)
		else:
			centroid = np.random.uniform(0, maxval)
		while (too_close(the_type, centroid, centroids, separation)):
			if the_type == 'g':
				centroid = np.random.uniform(-maxval, maxval, dims)
			else:
				centroid = np.random.uniform(0, maxval)
		centroids.append(centroid)
	return centroids

def create_data(the_type, centroids, num_points, dims, minvar, maxvar):
	'''
	Generates the data points.

	Parameters
	----------
	the_type : string
		'g' for Gaussian, 'r' for Radial.
	centroids : list
		List of cluster centroids or radii.
	num_points : integer
		Number of data points per cluster.
	dims : integer
		Dimensionality of the data.
	minvar : float
		Minimum intra-cluster variance.
	maxvar : float
		Maximum intra-cluster variance.

	Returns
	-------
	data : array, shape (len(centroids) * num_points, dims)
		List of dims-dimensional data points.
	'''
	data = []
	for centroid in centroids:
		variance = np.random.uniform(minvar, maxvar)
		for j in range(0, num_points):
			if the_type == 'g':
				data.append(np.random.normal(centroid, variance))
			else:
				x = np.random.uniform(-centroid, centroid)
				y = np.sqrt((centroid ** 2) - (x ** 2))
				if np.random.randint(2) == 0:
					y *= -1
				data.append(np.random.normal((x, y), variance))
	return np.array(data)

def calculate_affinities(data, neighborhood, sigma):
	'''
	Calculates pairwise affinities for the data.

	Arguments
	---------
	data : array, shape (N, M)
		Matrix of M-dimensional data points.
	neighborhood : float
		L2 distance threshold for computing affinities, anything outside of this
		threshold is set to 0.
	sigma : float
		Sigma value for computing affinities.

	Returns
	-------
	affinities : array, shape (N, N)
		Pairwise affinities for all data points.
	'''
	affinities = sklearn.metrics.pairwise.rbf_kernel(data, data, gamma = (1.0 / sigma))
	distances = sklearn.metrics.pairwise.pairwise_distances(data)

	# affinities and distances are the same dimensionality: (N, N)
	affinities[np.where(distances > neighborhood)] = 0.0
	return affinities

def write_data(data, affinities, raw, csv, mahout):
	'''
	Writes out the data and the affinities to text files.

	Parameters
	----------
	data : array, shape (N, M)
		Matrix of M-dimensional data points as row vectors.
	affinities : array, shape (N, N)
		Matrix of pairwise affinities.
	raw : string
		Path to the output file for the raw data (CSV format).
	csv : string
		Path to the output file for the affinity data (CSV format).
	mahout : string
		Path to the output file for the affinity data (Mahout format).
	Returns
	-------
	None
	'''
	# Write the raw data to CSV format.
	np.savetxt(raw, data, fmt = '%.5f', delimiter = ',')

	# Write the affinity data to CSV format.
	np.savetxt(csv, affinities, fmt = '%.5f', delimiter = ',')

	# Write the affinity data to Mahout format.
	f = open(mahout, 'w')
	N = np.size(affinities, axis = 0)
	for i in range(0, N):
		for j in range(0, N):
			f.write('%s,%s,%s\n' % (i, j, affinities[i, j]))
	f.close()

def main(arglist):
	'''
	Kicks off the main execution of the program.

	Parameters
	----------
	arglist : array
		A glorified dictionary of all the command-line arguments.

	Returns
	-------
	None
	'''
	# Step 0: Read the argument list.
	the_type, \
	clusters, \
	points_per_cluster, \
	dimensions, \
	separation, \
	abs_max, \
	neighborhood, \
	output_raw, \
	output_aff_csv, \
	output_aff_mahout, \
	min_var, \
	max_var, \
	sigma = arglist

	# Sanity check.
	if the_type == 'r' and dimensions != 2:
		print 'WARNING: You have chosen radial data, dimensions are restricted to 2.'
		dimensions = 2

	# Step 1: Define the cluster centroids.
	centroids = create_centroids(the_type, clusters, dimensions, separation, abs_max)

	# Step 2: Generate the data.
	data = create_data(the_type, centroids, points_per_cluster, dimensions, min_var, max_var)

	# Step 3: Calculate the data affinities.
	affinities = calculate_affinities(data, neighborhood, sigma)

	# Step 4: Write out the data and its affinities.
	write_data(data, affinities, output_raw, output_aff_csv, output_aff_mahout)

if __name__ == '__main__':
	# Read the command line arguments.
	retvals = read_args(sys.argv)
	main(retvals)