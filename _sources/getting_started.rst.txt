Getting Started
===============

This page details how to get started with montecarlo. Montecarlo is a package which was developed for the calculation of classical hamiltonians

Installation
------------
To install montecarlo, you will need an environment with the following packages:

* Python 3.7
* NumPy
* Matplotlib

Background
------------
.. math::
    \frac{H}{k} = -\frac{J}{k}\sum s_i s_{i+1}+\frac{\mu}{k}\sum s_i

Package
------------
Here's a sample code with the montecarlo package

.. code-block:: python

    import montecarlo

    lattice = montecarlo.spin_config_1D(n=2,temp=1)
    print(lattice)
    lattice.generate_plot(num_states=2)
    lattice = montecarlo.spin_config_1D(n=2,temp=1)
	

Once you have these packages installed, you can install montecarlo in the same environment using
::

    pip install -e .