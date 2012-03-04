import numpy as np
import sys
import matplotlib.pyplot as plot
import csv

# read the arguments - need two files
if len(sys.argv) < 3:
	quit('python parse.py [raw data file] [mahout output]')

# read the files
points = [[float(row[0]), float(row[1])] for row in csv.reader(open(sys.argv[1], "r"))]
labels = []
mapping = {}
colors = ['ko', 'yo', 'bo']
coloridx = 0
for row in csv.reader(open(sys.argv[2], "r"), delimiter = ' '):
	label = int(row[5])
	labels.append(label)
	if label not in mapping:
		mapping[label] = colors[coloridx]
		coloridx += 1

# now, graph the points
for i in range(0, len(points)):
	plot.plot(points[i][0], points[i][1], mapping[labels[i]])
plot.show()
