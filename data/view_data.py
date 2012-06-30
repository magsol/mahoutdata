import matplotlib.pyplot as plot
import numpy as np
import sys

def usage():
	'''
	plz 2 how use
	'''
	print '$> python view_data.py <format> <input file>'
	print '\t<format> raw\tGraphs the raw data in 2D format'
	print '\t<format> affinity\tGraphs the affinities as a heatmap'
	print '\t<format> mahout\tGraphs the affinities as a heatmap (Mahout format)'
	print '\t<input file>\tPath to file containing data'

def main(inputfile, format):
	'''
	Kicks off the main method.

	Parameters
	----------
	inputfile : string
		System path to the file containing the data.
	format : string
		[raw | affinity | mahout] Designates the input format.

	Returns
	-------
	None
	'''
	data = np.loadtxt(inputfile, delimiter = ',')
	if format == 'raw':
		plot.plot(data[:, 0], data[:, 1], '.')
	elif format == 'affinity':
		plot.imshow(data)
	else:
		# A little more involved.
		N = np.size(data, axis = 0)
		dims = data[N - 1, 0]
		toplot = np.zeros((dims + 1, dims + 1))
		for t in range(0, N):
			i = data[t, 0]
			j = data[t, 1]
			val = data[t, 2]
			toplot[i, j] = val
		plot.imshow(toplot)
	plot.show()

# Plots the raw data.
# Shows the heatmap for the affinity matrix.
if __name__ == '__main__':
	if len(sys.argv) != 3 or (sys.argv[1] != 'raw' and sys.argv[1] != 'affinity' and sys.argv[1] != 'mahout'):
		usage()
		quit()
	main(sys.argv[2], sys.argv[1])