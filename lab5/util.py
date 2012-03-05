import getopt
import matplotlib.pyplot as plot
import matplotlib.image as mpimg
import matplotlib.cm as cm
import numpy as np

true_data = np.load('mysterious.npy')

# We'll set up a class to make this a little easier.
class Particle:
  def __init__(self, iterations, limitx, limity, limitv):
    self.x = np.zeros(iterations + 1)
    self.x[0] = np.random.uniform(0, limitx)
    self.y = np.zeros(iterations + 1)
    self.y[0] = np.random.uniform(0, limity)
    self.vx = np.zeros(iterations + 1)
    self.vx[0] = np.random.uniform(0, limitv)
    self.vy = np.zeros(iterations + 1)
    self.vy[0] = np.random.uniform(0, limitv)
    self.px = np.zeros(iterations + 1)
    self.px[0] = self.x[0]
    self.py = np.zeros(iterations + 1)
    self.py[0] = self.y[0]

def plotIteration(particles, iteration, data, bestx, besty):
  '''
  Plots a figure with the current particles (black circles) and
  current best global position, saving the graph as a PNG file
  you can look at later.
  '''
  plot.hold(True)
  plot.imshow(data, cmap = cm.gray)
  for particle in particles:
    plot.scatter(particle.x[iteration], particle.y[iteration], c = 'b', marker = 'o')
  plot.scatter(bestx, besty, c = 'y', marker = 'x')
  plot.savefig('iteration_%s' % iteration)
  plot.close()

def usage():
  print ' $> python lab5.py [-p -v -c -s -i -w -h]'
  print '\t-i <#>\tNumber of iterations to run the simulation [10]'
  print '\t-p <#>\tNumber of particles for the simulation [20]'
  print '\t-v <#>\tMaximum velocity of a particle [10]'
  print '\t-c <#>\tCognitive parameter [2]'
  print '\t-s <#>\tSocial parameter [2]'
  print '\t-w <#>\tInertia parameter [1]'
  print '\t-h\tPrint this help!'

def readArgs(args):

  # Set up the defaults.
  maxV = 10
  iterations = 10
  numparticles = 20
  c = 2
  s = 2
  w = 1.0

  try:
    optlist, arglist = getopt.getopt(args[1:], 'i:p:v:c:s:w:h')
  except getopt.GetoptError, err:
    print str(err)
    usage()
    sys.exit(2)

  for key, val in optlist:
    if key == '-i':
      iterations = np.abs(int(val))
    elif key == '-p':
      numparticles = np.abs(int(val))
    elif key == '-v':
      maxV = np.abs(float(val))
    elif key == '-c':
      c = np.abs(float(val))
    elif key == '-s':
      s = np.abs(float(val))
    elif key == '-w':
      w = np.abs(float(val))
    elif key == '-h':
      usage()
      quit()

  # Initialize the particles.
  data = np.zeros(true_data.shape)
  width, height = data.shape
  particles = np.array([Particle(iterations, width, height, maxV) \
                      for i in range(0, numparticles)])

  # Return everything.
  return [data, particles, iterations, c, s, w, maxV]
