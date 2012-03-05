from util import *
import sys
import numpy as np

def objective(x, y, data):
  '''
  This is our objective function. It evaluates how good a 
  job we're doing, and tells us if we're at a good spot. It will
  also reveal portions of the data that your particles have explored!
  '''
  data[x, y] = true_data[x, y]
  return data[x, y]

def updateGlobalBest(particles, iteration, data):
  '''
  Update rule for the global best. Of all the particles' personal
  bests (p-elements), this selects the one that is best among those and
  returns its x,y coordinates.

  Arguments
  =========
  particles: the array of particle objects
  iteration: the integer iteration number (1 to # of iterations, inclusive)
  data: the matrix consisting of our search space

  Returns
  =======
  array: a two-element array corresponding to the [x, y] coordinates of the
    best global position
  '''

  ###################
  # -- FIX ME!!! -- #
  ###################

  return [0, 0]

def updateVelocity(particle, iteration, r1, r2, c, s, w, gx, gy, vmax):
  '''
  Update rule for the particle velocities. This happens before everything else,
  so it is somewhat complicated with so many parameters involved. This calculates
  the new velocity for each particle.

  Arguments
  =========
  particle: a single particle object whose velocity we wish to update
  iteration: integer iteration number
  r1: random uniform [0, 1]
  r2: random uniform [0, 1]
  c: the cognitive parameter: controls how self-aware the particle is
  s: the social parameter: controls how much influence other particles have on this one
  w: the inertia parameter: controls how much influence previous velocities have on
    current velocity
  gx: the current globally-best x-coordinate
  gy: the current globally-best y-coordinate
  vmax: the maximum allowed velocity of a particle

  Returns
  =======
  array: a two-element array corresponding to the velocity in the x-direction
    and the y-direction [vx, vy]
  '''

  ###################
  # -- FIX ME!!! -- #
  ###################

  return [0, 0]

def updatePosition(particle, iteration, xmax, ymax):
  '''
  Update rule for the particle's position in x,y space.

  Arguments
  =========
  particle: the current particle whose position we wish to update
  iteration: integer iteration number
  xmax: the maximum x-value a particle can have [0, xmax] inclusive
  ymax: the maximum y-value a particle can have [0, ymax] inclusive

  Returns
  =======
  array: a two-element array corresponding to the [x, y] coordinates of
    the particle's new location
  '''

  ###################
  # -- FIX ME!!! -- #
  ###################

  return [0, 0]

def updateParticleBest(particle, iteration, data):
  '''
  Update rule for the particle's current personal best.
  
  Arguments
  =========
  particle: the current particle whose personal best position we wish to update
  iteration: integer iteration number
  data: the matrix representing our total search space, and for evaluating the
    objective function

  Returns
  =======
  array: a two-element array corresponding to the particle's new personal best
    [x, y] position
  '''

  ###################
  # -- FIX ME!!! -- #
  ###################

  return [0, 0]

def main(args):
  data, \
  particles, \
  iterations, \
  cognitive, \
  social, \
  inertia, \
  maxvelocity = readArgs(sys.argv)

  # This is how we initialize the global best positions.
  gx, gy = updateGlobalBest(particles, 0, data)

  # We'll plot the initialization, even though it won't reveal much.
  plotIteration(particles, 0, data, gx, gy)

  # Start the simulation loop!
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

    # After updating all the particles, update the global best position.
    gx, gy = updateGlobalBest(particles, i, data)

    # Shrink the inertia.
    inertia = np.max([0, inertia - (inertia / iterations)])

    # If you want to create iteration-by-iteration plots, uncomment the following line:
    # (this will slow down the simulation considerably and create lots of files!)
    #plotIteration(particles, i, data, gx, gy)

  # If you only want to plot the final version, leave the previous line commented
  # out and uncomment this one (this gives a HUGE speed boost):
  #plotIteration(particles, iterations, data, gx, gy)

if __name__ == '__main__':
  main(sys.argv)
