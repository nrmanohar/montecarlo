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

    git clone git@github.com:nrmanohar/montecarlo.git
    cd montecarlo
    pip install -e .

Theory
-------

Background and Physics
````````````````````````
.. math::
    \frac{H}{k} = -\frac{J}{k}\sum s_i s_{i+1}+\frac{\mu}{k}\sum s_i


This is the equation of the 1D spin lattice hamiltonian, where s is the spin of each state 
on the lattice state. This can be used to compute the energy levels of a spin lattice structure, 
and by extension the probability of it occuring using the Boltzmann distribution. However, these 
structures have other important charactaristics, like magnetization. Using that, we can compute 
the average energy and average magnetization of all states of a certain size, and from there 
determine the heat capacity and magnetic susceptibility. Magnetization can be written as such

.. math::
    M = \sum s_i

And the relative probability can be written as the following

.. math::
    P(\alpha) = e^{-E(\alpha)/{kT}}

However, this is unnormalized, and thus will give incorrect values. For discrete energies, the normalization factor is

.. math::
    Z = \sum e^{-E(\alpha)/{kT}}

Similarly, for a continuous energy distribution, the normalization factor is

.. math::
    Z = \int e^{-E(\alpha)/{kT}}

Which makes the actual probability of each state

.. math::
    P(\alpha) = \frac{1}{Z} e^{-E(\alpha)/{kT}}

The heat capacity can be calculated using expectation values of energy as follows.

.. math::
    C = \frac{\langle E^2 \rangle - \langle E \rangle^2}{kT^2}

where

.. math::
    \langle E\rangle = \sum P(\alpha)E(\alpha)

Magnetic susceptibility can be calculated as follows, in a very similar manner to heat capacity

.. math::
    \chi =\frac{\langle M^2 \rangle - \langle M \rangle^2}{kT}


This package can calculate all these values exactly, using the formulas listed above.

Montecarlo and Metropolis
``````````````````````````
However, calculating these values precisely is computationaly taxing, so we can approximate 
using the montecarlo method. Essentially, the goal is to use a random lattice to approximate 
the total energy distribution. However, this doesn't include probabilities, and so it wouldn't 
generate a good plot. The key was the phase transition probability. 

.. math::
    W(\alpha\rightarrow \beta) = e^{-(E(\beta)-E(\alpha))/kT}

The key is when to keep a state and it's associated energy, and when not to, and when to 
use that energy to compare other energies. The tester lattice is a random lattice. Then it'll 
sweep through each lattice site and flip it's spin and calculate it's energy. If the energy is 
lower than the energy of the comparison, it's more probable, and so the state will be kept. If 
the state has a higher energy, we use the comparison used above, which will generate a number 
between zero and one, and then compare it to a random number between zero and one. If the probabilty 
of the phase change is higher than the generated random number, then we keep that state and use that 
state as the reference energy to compare to.

Examples
------------
Here's a sample code with the montecarlo package

.. code-block:: python

    from montecarlo import *

    lattice = spin_config_1D(n=2,temp=1)
    print(lattice)
    lattice.generate_plot()

which generates the output

::

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

However, we can also simulate a simular plot using the metropolis sampling. The default metro_plot() function generates a plot similar to the default generate_plot() method. Continuing from the previous code block
(note, the outputs won't be exactly the same)

.. code-block:: python

    metro_plot()

generates an output similar to	

.. image:: Plot2.jpg
  :width: 400
  :alt: Metro plot

As you can see, this is an approximation. We can make this approximation better by increasing the number of sweeps we include.

.. code-block:: python

    metro_plot(sweeps = 10000)

generates the output

.. image:: Plot3.jpeg
  :width: 400
  :alt: Metro plot 2

note how the output is smoother. More sweeps allows you to be more accurate with your plots, at the cost of a higher computation time.
