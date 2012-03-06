from util import *
import sys
import numpy as np

# Now some methods to help with the simulation.
def objective(x, y, data):
  '''
  This is our objective function. It evaluates how good a 
  job we're doing, and tells us if we're at a good spot.
  '''
  data[x, y] = true_data[x, y]
  return data[x, y]

def updateGlobalBest(particles, iteration, data):
  '''
  Finds the particle with the best position so far. 
  '''
  bestval = -1
  bx = 0
  by = 0
  for particle in particles:
    newval = objective(particle.px[iteration], particle.py[iteration], data)
    if newval > bestval:
      bestval = newval
      bx = particle.px[iteration]
      by = particle.py[iteration]
  return [bx, by]

def updateVelocity(particle, iteration, r1, r2, c, s, w, gx, gy, vmax):
  '''
  Given all the parameters, this updates the particle's velocity.
  '''
  vx = w * particle.vx[iteration - 1] + \
      r1 * c * (particle.px[iteration - 1] - particle.x[iteration - 1]) + \
      r2 * s * (gx - particle.x[iteration - 1])
  vy = w * particle.vy[iteration - 1] + \
      r1 * c * (particle.py[iteration - 1] - particle.y[iteration - 1]) + \
      r2 * s * (gy - particle.y[iteration - 1])
  if np.abs(vx) > vmax:
    if vx < 0:
      vx = -vmax
    else:
      vx = vmax
  if np.abs(vy) > vmax:
    if vy < 0:
      vy = -vmax
    else:
      vy = vmax
      
  return [vx, vy]

def updatePosition(particle, iteration, xmax, ymax):
  '''
  Given the particle and the current iteration, this updates the
  particle's position.
  '''
  x = np.min([xmax, np.max([0, particle.x[iteration - 1] + particle.vx[iteration]])])
  y = np.min([ymax, np.max([0, particle.y[iteration - 1] + particle.vy[iteration]])])
  return [x, y]

def updateParticleBest(particle, iteration, data):
  '''
  Given the particle and the data, this updates the particle's current
  best coordinates.
  '''
  px = particle.x[iteration]
  py = particle.y[iteration]
  oldpx = particle.px[iteration - 1]
  oldpy = particle.py[iteration - 1]
  if objective(px, py, data) < objective(oldpx, oldpy, data):
    return [oldpx, oldpy]
  else:
    return [px, py]

def main(args):
  data, \
  particles, \
  iterations, \
  cognitive, \
  social, \
  inertia, \
  maxvelocity = readArgs(sys.argv)

  # First, we need to initialize the best global position. Formally, this is
  # the particle i with the best value for p. But since p was just initialized
  # to be the particle's current position, then this amounts to whatever particle
  # is currently sitting on the best value.
  gx, gy = updateGlobalBest(particles, 0, data)

  # Now, if you want, we can plot our current setup, but it's not going to 
  # look particularly good since we haven't revealed much of the space.
  plotIteration(particles, 0, data, gx, gy)

  # Let's start the simulation, shall we?
  for i in range(1, iterations + 1):
    for p in particles:
      # Generate our two random coefficients. This comprises the stochastic
      # portion of this optimization algorithm.
      r1, r2 = np.random.uniform(0, 1, 2)

      # Do all our update rules!
      p.vx[i], p.vy[i] = \
        updateVelocity(p, i, r1, r2, cognitive, social, inertia, gx, gy, maxvelocity)
      p.x[i], p.y[i] = updatePosition(p, i, data.shape[0] - 1, data.shape[1] - 1)
      p.px[i], p.py[i] = updateParticleBest(p, i, data)

    gx, gy = updateGlobalBest(particles, i, data)

    # Shrink the inertia.
    inertia = np.max([0, inertia - (inertia / iterations)])

    # Plot the current iteration.
    #plotIteration(particles, i, data, gx, gy)
  plotIteration(particles, iterations, data, gx, gy)

if __name__ == '__main__':
  main(sys.argv)
