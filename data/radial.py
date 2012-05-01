import sys
import numpy as np
import util

'''
This scripts generates concentric circles of data, where the points
lie normally distributed on the respective radii of each circle. This
is useful for testing more specialized clustering algorithms, as traditional
ones that operate in the euclidean space tend to not fare too well with
data such as this.
'''

def too_close(radius, radii, threshold):
	'''
	Defines a distance metric: we want the radii to be more or less
	well-separated with respect to some threshold, so this ensures that 
	they are all some amount away from each other.
	'''
	for value in radii:
		if np.abs(radius - value) < threshold:
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
maxvar = util.read_args(sys.argv, 'radial')

# NOTE: Currently dimensions is hard-coded at 2, since sampling
# points from an n-dimensional hypersphere is not exactly trivial.
# Hopefully a future update of this script with enable this feature.
# For now...sorry brah.

# Generate the radii.
radii = []
data = []
for i in range(0, clusters):
	radius = np.random.uniform(0, maximum)
	while (too_close(radius, radii, separation)):
		radius = np.random.uniform(0, maximum)
	radii.append(radius)

	# Generate the points along each circle's radius.
	variance = np.random.uniform(minvar, maxvar)
	for j in range(0, points):
		# Sample the x-value from a uniform distribution.
		x = np.random.uniform(-radius, radius)

		# Solve for y. (since equation of a circle is x^2 + y^2 = r^2)
		y = np.sqrt((radius ** 2) - (x ** 2))

		# However, since this is a circle, y could potentially be negative.
		# Flip a coin to see which side y is on.
		if np.random.randint(2) == 0:
			y *= -1

		# Finally, add some gaussian noise to the point.
		data.append(np.random.normal((x, y), variance))

# Write out the data.
data = np.array(data)
np.savetxt(output, data, fmt = '%s', delimiter = ',')
