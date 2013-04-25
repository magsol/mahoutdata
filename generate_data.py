import argparse
import numpy as np
import sklearn.datasets as datasets
import sklearn.metrics.pairwise as pairwise

def write_data(data, affinities, raw, mahout):
    """
    Writes out the data and the affinities to text files.

    Parameters
    ----------
    data : array, shape (N, M)
        Matrix of M-dimensional data points as row vectors.
    affinities : array, shape (N, N)
        Matrix of pairwise affinities.
    raw : string
        Path to the output file for the raw data (CSV format).
    mahout : string
        Path to the output file for the affinity data (Mahout format).

    Returns
    -------
    None
    """
    # Write the raw data to CSV format.
    np.savetxt(raw, data, fmt = '%.6f', delimiter = ',')

    # Write the affinity data to Mahout format.
    f = open(mahout, 'w')
    N = np.size(affinities, axis = 0)
    for i in range(0, N):
        for j in range(0, N):
            f.write('%s,%s,%s\n' % (i, j, affinities[i, j]))
    f.close()

def calculate_affinities(data, neighborhood, sigma):
    """
    Calculates pairwise affinities for the data.

    Parameters
    ----------
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
    """
    affinities = pairwise.rbf_kernel(data, data, gamma = (1.0 / (2 * sigma * sigma)))
    distances = pairwise.pairwise_distances(data)

    # affinities and distances are the same dimensionality: (N, N)
    affinities[np.where(distances > neighborhood)] = 0.0
    return affinities

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Mahout Spectral Clustering Data Generation', \
        epilog = 'lol spectral', add_help = 'How to use', \
        prog = 'python generate_data.py <options>')
    parser.add_argument('-t', '--type', required = True, choices = ['circles', 'blobs', 'moons'],
        help = 'Type of data to generate.')

    # Optional arguments.
    parser.add_argument('-n', '--n_points', default = 100, type = int,
        help = 'Number of data points per cluster. [DEFAULT: 100]')
    parser.add_argument('-s', '--sigma', default = 0.5, type = float,
        help = 'Amount of noise to add to the data. [DEFAULT: 0.5]')
    parser.add_argument('-c', '--clusters', default = 3, type = int,
        help = 'If "blobs", number of clusters to generate. [DEFAULT: 3]')
    parser.add_argument('-r', '--rbfkernel', default = 1.0, type = float,
        help = 'RBF kernel sigma value to use in computing affinities. [DEFAULT: 1.0]')
    parser.add_argument('-d', '--distance', default = 2.0, type = float,
        help = 'Minimum pointwise distance threshold, beyond which affinities are set to 0. [DEFAULT: 2.0]')

    # Output arguments.
    parser.add_argument('-o1', '--out_raw', default = 'raw.txt',
        help = 'Output path for the raw CSV data. [DEFAULT: raw.txt]')
    parser.add_argument('-o2', '--out_aff', default = 'aff.txt',
        help = 'Output path for the Mahout-style affinity data. [DEFAULT: aff.txt]')

    args = vars(parser.parse_args())

    # Generate the data.
    X = None
    y = None
    if args['type'] == "circles":
        X, y = datasets.make_circles(n_samples = args['n_points'] * 2,
            shuffle = False, noise = args['sigma'], factor = 0.3)
    elif args['type'] == "blobs":
        X, y = datasets.make_blobs(n_samples = args['n_points'] * args['clusters'],
            centers = args['clusters'], cluster_std = args['sigma'], shuffle = False)
    else:
        X, y = datasets.make_moons(n_samples = args['n_points'] * 2,
            shuffle = False, noise = args['sigma'])

    # Calculate affinities.
    A = calculate_affinities(X, args['distance'], args['rbfkernel'])

    # Write everything out.
    write_data(X, A, args['out_raw'], args['out_aff'])
