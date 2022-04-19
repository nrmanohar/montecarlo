Getting Started
===============

This page details how to get started with montecarlo. Montecarlo is a package which was developed for the calculation of classical hamiltonians

Installation
------------
To install montecarlo, you will need an environment with the following packages:

* Python 3.7
* NumPy
* Matplotlib

Once you have these packages installed, you can install montecarlo in the same environment using
::

    pip install -e .

Background
------------
.. math::
    \frac{H}{k} = -\frac{J}{k}\sum s_i s_{i+1}+\frac{\mu}{k}\sum s_i


This is the equation of the 1D spin lattice hamiltonian. This can be used to compute the energy levels of a spin lattice structure, and by extension the probability of it occuring using the Boltzmann distribution

Package
------------
Here's a sample code with the montecarlo package

.. code-block:: python

    import montecarlo

    lattice = montecarlo.spin_config_1D(n=2,temp=1)
    print(lattice)
    lattice.generate_plot(num_states=8)

which generates the output

.. code-block::
    
    States: [[-1, -1], [-1, 1], [1, -1], [1, 1]]
    Energies: [1.7999999999999998, -3.9999999999999996, -4.0, 6.199999999999999]
    Magnetizations: [-2, 0, 0, 2]
    Probabilities: [0.0015114612660751597, 0.4992349910051053, 0.4992349910051055, 1.8556723713926915e-05]
    Average Energy: -3.9910442460748814
    Average Magnetization: -0.0029858090847224654
    Heat Capcity: 0.0526959929976023
    Magnetic Susceptibility: 0.0526959929976023
    Constants
	    Boltzmann Constant is: 1
	    J is: -2
	    mu is: 1.1
	    Temperature is: 1

.. image:: Plot1.jpg
  :width: 400
  :alt: Ising plot
	