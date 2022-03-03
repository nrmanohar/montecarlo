"""
Unit and regression test for the montecarlo package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import montecarlo


def test_montecarlo_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "montecarlo" in sys.modules
def test_montecarlo_state():
    generator = montecarlo.spin_config_1D(n=2)
    assert generator.states == [[-1, -1], [-1, 1], [1, -1], [1, 1]]
def test_montecarlo_average_energy():
    tester = montecarlo.spin_config_1D(n=2,temp=1)
    assert round(tester.avg_eng,8) == -3.99104425
def test_montecarlo_average_mag():
    tester = montecarlo.spin_config_1D(n=2,temp=1)
    assert round(tester.avg_mag,8) == -0.00298581
def test_montecarlo_heat_cap():
    tester = montecarlo.spin_config_1D(n=2,temp=1)
    assert round(tester.heat_capacity,8) == 0.05269599
def test_montecarlo_mag_sus():
    tester = montecarlo.spin_config_1D(n=2,temp=1)
    assert round(tester.mag_sus,8) == 0.00611116


    