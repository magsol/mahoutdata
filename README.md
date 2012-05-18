# Scripts

By: Shannon Quinn

## License

As a default rule of thumb, unless otherwise stated, everything I release falls under the Apache 2.0 license, as stated:

> Copyright 2012 Shannon Quinn
> 
> Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
> 
>  http://www.apache.org/licenses/LICENSE-2.0
> 
> Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permission and limitations under the License.

## Description of Files

I'll maintain a list here of the files in this repository and what they do.

- **parse.py**: A script for taking a text version of a Java HashMap (output from an Apache Mahout MapReduce job) and converting it to a histogram.
- **sample_arb_dist_with_uniform.py**: This was a venture into sampling arbitrary distributions, given that one's API (cough PHP cough) had only uniform random number generators.
- **particle.js**: An experiment with HTML5 canvas. You can create a simulation of particles which fly around the canvas with a certain amount of gravity. When a critical mass of particles balls up in a critical radius, they explode. It's pretty neat.
- **lab5/**: This folder contains an assignment I wrote for the Spring 2012 rendition of Cell & Sytems Modeling, a core course for the Joint CMU-UPitt Ph.D. in Computational Biology program. It lays out the framework for a naive Particle Swarm Optimization implementation, leaving the students to fill in the update functions.
- **data/**: This folder was moved from a different repository of mine to here, as it seemed more fitting in this scripts repository. These scripts generate data specifically designed to be tested with some clustering algorithms we're working on. Once the raw data has been generated, there is also a script that converts the raw data to a format that these algorithms as implemented in Apache Mahout will read as input. Contact me if you have any questions about this.
- **garmin/**: This folder contains XML parsing scripts for reading the data files from Garmin GPS watches and plotting them, the main idea being to give the user more of an idea of their running trends than the basic first-order statistics offered by Garmin Connect.
