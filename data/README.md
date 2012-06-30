# Data Generation Scripts

By: Shannon Quinn

## Overview

These scripts were mainly created for the purpose of troubleshooting and checking the spectral clustering library in Apache Mahout, but can be used for any purpose requiring some random data. Currently, here's how things work:

1. `generate_data.py` is the one-stop shop for creating gaussian or radial clusters of data. There are tons of parameters to choose from in tweaking your dataset (though they all have reasonable defaults), so run the script with the "-h" flag first to get a feel for what it can do. It will also output the raw data and the data affinities to text files in standard CSV formats, and in the format Mahout expects (as of version 0.7), to make troubleshooting the datasets much simpler.

2. `view_data.py` is a purely troubleshooting script that will plot the raw data you've generated in the previous step, in addition to plotting the affinities also created. You can use this script to assure yourself that the affinities in the CSV format and in the Mahout formats are identical, and that you know what the data looks like.

3. `solve.py` implements in a traditional fashion what Mahout implements in MapReduce: spectral k-means clustering of the affinity data. It will then plot the clustering results so you know what to expect from Mahout's output.

To run these scripts, you need:
- Python 2.7+
- NumPy 1.5+, SciPy 0.10+ (core computations)
- matplotlib 1.1+ (viewing the data)
- scikit-learn 0.11+ (computing affinities, performing clustering)
