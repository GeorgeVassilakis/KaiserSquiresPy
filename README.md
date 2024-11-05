# SMPy (Shear Mapping in Python)

## Overview
SMPy is a Python-based toolkit designed for astrophysicists and cosmologists, facilitating the construction of convergence maps from shear data. This tool leverages the power of Python to provide an accessible and efficient way to analyze gravitational lensing effects, particularly focusing on the mapping of dark matter distribution in galaxy clusters.

## Features
- User-friendly interface for data handling and visualization.
- Modular codebase that allows multiple convergence mapping methods/techniques.
   - Currently uses Kaiser-Squires Inversion (1993).
   - Aperture-mass mapping is currently under development.
- Compatibility with standard astrophysical data formats.

## Installation

1. **Prerequisites**: Ensure you have Python 3.x installed on your system. SMPy also requires `numpy`, `scipy`, `pandas`, `astropy`, and `matplotlib` for numerical computations and visualizations.

2. **Clone the Repository**: Clone the SMPy repository to your local machine using git:

   ```bash
   git clone https://github.com/GeorgeVassilakis/SMPy.git

3. **Install the Package:** Install SMPy using setup.py:

   ```bash
   pip install .

## How to Run
### With runner script
1. **Edit your `example_config.yaml` configuration file**
   - This file defines many parameters.
   - Most importantly, it defines the input/output paths and file-specific columns like ra, dec, g1, g2, and weights.
   - It also controls various visualization parameters like titles, color scaling, and smoothing parameters.

2. **Run the runner.py script:** Use the -c or -config flag to pass your .yaml file
   
   ```bash
   python runner.py -c /path/to/example_config.yaml

### With Jupyter Notebook
1. Import the run module:
`from smpy import run`

2. Edit the `example_config.yaml` configuration file
  
3. Define config path and run:

   `config_path = '/path/to/SMPy/smpy/configs/example_config.yaml'`

   `run.run(config_path)`

## Example Kaiser Squires Convergence Map
![Kaiser Squires Convergence Map](examples/outputs/simulation_testing_kaiser_squires_e_mode.png)
