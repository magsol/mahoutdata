// A great deal of this code was inspired by Codeflow.
// http://codeflow.org/entries/2010/aug/22/html5-canvas-and-the-flying-dots/
// I just added the bit where the particles explode :)

var Universe = function() { this.init.apply(this, arguments); };
Universe.prototype = {

  init: function(numParticles, interval, maxVelocity, maxAcceleration, criticalMass, criticalRadius) {
    var canvas = document.getElementById('particles');
    var context = canvas.getContext('2d');

    // Set the arguments.
    if (typeof criticalMass == 'undefined' || criticalMass > numParticles) {
      criticalMass = -1;
    }
    if (criticalMass <= 0 || typeof criticalRadius == 'undefined' || criticalRadius <= 0) {
      criticalRadius = -1;
    }

    // Create the particles.
    var particles = [];
    for (var i = 0; i < numParticles; ++i) {
      particle = new Particle(canvas, maxVelocity, maxAcceleration);
      particles.push(particle);
    }

    // Run the simulation!
    setInterval(function() {
      context.clearRect(0, 0, canvas.width, canvas.height);
      var criticalSet = new Array(numParticles);
      var explosion = new Vector(0, 0);
      var count = 0;
      for (var i = 0; i < numParticles; ++i) {
        var p1 = particles[i];
        for (var j = 0; j < numParticles; ++j) {
          var p2 = particles[j];
          var vector = p1.position.subtract(p2.position);
          var distance = vector.magnitude();
          if (criticalMass > 0) {
            if (distance < (criticalRadius * 2)) {
              if (isNaN(criticalSet[j])) {
                criticalSet[j] = 1;
              } else {
                criticalSet[j] += 1;
                if (i == (numParticles - 1) && criticalSet[j] >= criticalMass) {
                  explosion.iadd(particles[j].position);
                  count += 1;
                }
              }
            } else {
              criticalSet[j] = 0;
            }  
          }

          if (i <= j) {
            continue;
          }
          // Acceleration between the two particles is proportional to
          // the inverse of the distance between them squared (since masses
          // are currently unitary, the force is indeed 1/d^2)
          vector.idivide(distance * distance);

          // Apply the change to the acceleration of the particle.
          p2.acceleration.iadd(vector);
          p1.acceleration.isubtract(vector);
        }
      }
      
      // This next loop is PURELY for calculating the explosion!
      // FINALLY do the update on the particles' positions!
      if (criticalMass > 0 && count >= criticalMass) {
        explosion.idivide(count);
      }
      for (var i = 0; i < numParticles; ++i) {
        if (criticalMass > 0 && count >= criticalMass) {
          var direction = explosion.subtract(particles[i].position);
          var distance = direction.magnitude() * 1000;
          direction.idivide(distance * distance);
          particles[i].acceleration = new Vector(direction.x, direction.y);
          particles[i].velocity.iadd(direction);
        }
        particles[i].step();
        particles[i].draw();
      }
    }, interval);
  }
}

var Particle = function() { this.init.apply(this, arguments); };
Particle.prototype = {
  canvas: null,
  position: null,
  velocity: null,
  acceleration: null,
  mass: 1,
  radius: 2,
  maxVelocity: -1,
  maxAcceleration: -1,

  init: function(canvas, maxVelocity, maxAcceleration) {
    // Initialize the variables.
    this.canvas = canvas;
    this.position = new Vector(
      randomInteger(0, this.canvas.width),
      randomInteger(0, this.canvas.height)
    );
    this.velocity = new Vector(0, 0);
    this.acceleration = new Vector(0, 0);
    this.maxVelocity = (typeof maxVelocity == 'undefined') ? -1 : maxVelocity;
    this.maxAcceleration = (typeof maxAcceleration == 'undefined') ? -1 : maxAcceleration;
  },

  step: function() {
    // Check if the acceleration is even a valid number.
    this.acceleration.validate();

    // Check if the acceleration is too fast.
    var accel = this.acceleration.magnitude();
    if (this.maxAcceleration > 0 && accel > this.maxAcceleration) {
      this.acceleration.idivide(accel / this.maxAcceleration);
    }

    // Update the velocity.
    this.velocity.iadd(this.acceleration);

    // Check if the velocity is too fast.
    var speed = this.velocity.magnitude();
    if (this.maxVelocity > 0 && speed > this.maxVelocity) {
      this.velocity.idivide(speed / this.maxVelocity);
    }

    // Update the position and zero out the acceleration.
    this.position.iadd(this.velocity);
    this.acceleration.zero();

    // Ensure we are still within the canvas borders.
    if (this.position.x < 0) {
      this.position.x = 0;
      this.velocity.x *= -1;
    } else if (this.position.x > this.canvas.width) {
      this.position.x = this.canvas.width;
      this.velocity.x *= -1;
    }
    if (this.position.y < 0) {
      this.position.y = 0;
      this.velocity.y *= -1;
    } else if (this.position.y > this.canvas.height) {
      this.position.y = this.canvas.height;
      this.velocity.y *= -1;
    }
  },

  draw: function() {
    var context = this.canvas.getContext('2d');
    context.beginPath();
    context.arc(this.position.x, this.position.y, this.radius, 0, Math.PI * 2, false);
    context.fill();
  }
}

var Vector = function() { this.init.apply(this, arguments); };
Vector.prototype = {
  x: 0,
  y: 0,

  init: function(x, y) {
    this.x = x;
    this.y = y;
  },

  subtract: function(vector) {
    return new Vector(
      this.x - vector.x,
      this.y - vector.y
    );
  },

  isubtract: function(vector) {
    this.x -= vector.x;
    this.y -= vector.y;
  },

  iadd: function(vector) {
    this.x += vector.x;
    this.y += vector.y;
  },

  magnitude: function() {
    return Math.sqrt((this.x * this.x) + (this.y * this.y));
  },

  idivide: function(scalar) {
    this.x /= scalar;
    this.y /= scalar;
  },

  zero: function() {
    this.x = 0;
    this.y = 0;
  },

  validate: function() {
    if (isNaN(this.x + this.y)) {
      this.x = 0;
      this.y = 0;
    }
  }
}

function randomInteger(low, high) {
  return Math.floor((Math.random() * (high - low)) + low);
}

function main() {
  var universe = new Universe(300, 20, 20, -1, 20, 100);
}
