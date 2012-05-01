import sys
import getopt

def usage(the_type):
	'''
	Defines the command line parameters for using this script
	to generate toy data for clustering.
	'''
	print '$> python %s.py [args]' % the_type
	print '\nAll parameters are optional (defaults in brackets)'
	print '\t-c <#>\t\tNumber of clusters from which to generate points [3]'
	print '\t-p <#>\t\tNumber of points per cluster [100]'
	print '\t-d <#>\t\tDimensionality of the data [2]'
	print '\t-o <file>\tFilename for the output of the raw data [%s_output.txt]' % the_type
	print '\t-s <#>\t\tMinimum separation (euclidean norm) between %s centroids [3]' % the_type
	print '\t-m <#>\t\tAbsolute maximum value for any generated data point [10]'
	print '\t--min-var <#>\tMinimum intra-cluster variance [0.5]'
	print '\t--max-var <#>\tMaximum intra-cluster variance [1.0]'
	print '\t-h\t\tPrint this help!'

def read_args(args, the_type):
	'''
	Reads and processes the command-line arguments.
	'''

	# HERE ARE THE DEFAULT VALUES FOR EACH COMMAND LINE ARGUMENT
	clusters = 3
	points_per_cluster = 100
	output = '%s_output.txt' % the_type
	separation = 3
	dimensions = 2
	abs_max = 10
	min_var = 0.5
	max_var = 1
	
	try:
		optlist, args = getopt.getopt(args[1:], 'hc:p:s:d:m:o:', \
			['max-var=', 'min-var='])
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)

	for key, val in optlist:
		if key == '-c':
			clusters = int(val)
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
		elif key == '--min-var':
			min_var = float(val)
		elif key == '--max-var':
			max_var = float(val)
		elif key == '-h':
			usage(the_type)
			sys.exit(0)
	return [clusters, points_per_cluster, output, separation, \
			abs_max, dimensions, min_var, max_var]