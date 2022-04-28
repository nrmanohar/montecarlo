"""Contains the funcions to complete montecarlo calculations and graphing"""
from .hamiltonian import *
import numpy as np
import matplotlib.pyplot as plt
plt.clf()
plt.cla()
plt.close()
import random
import math

def average(list):
    """Computes the average of any input list, in our case the list of energies

    :param list: Any list (of numbers)
    :type list: list
    :return: The arithmetic average of the list
    :rtype: float or int
    """
    sum=0
    for i in list:
        sum+=i
    return sum/len(list)

def sweep(state, mu=1.1, k=1, J=-2, T=1):
    """Computes energies and magnetization of each sweep of a given state and returns a list of them

    :param state: The state to be sweeped
    :type list: list
    :param mu: the magnetic constant, defualts to 1.1
    :type mu: float or int
    :param k: the boltzmann constant, defaults to 1
    :type k: float or int
    :param J: the ferromagnetic constant, defaults to -2
    :type J: float or int
    :param T: the temperature your state is in, defaults to 1
    :type T: float or int
    :return: A list of lists, the first list is the list of energies, the second of magnetizations
    :rtype: list
    """
    energies = []
    mags = []
    states = []
    states.append(state)
    energies.append(spin_energy(J,mu,k,state))
    sweeper = state.copy()
    for i in range(len(sweeper)):
        if sweeper[i]==-1:
            sweeper[i]=1
        elif sweeper[i]==1:
            sweeper[i]==-1
        energy_two = spin_energy(J,mu,k,sweeper)
        avg_eng = sum(energies)/len(energies)
        if energy_two < energies[0]:
            energies.append(energy_two)
            states.append(sweeper)
        else:
            prob = math.exp((-energy_two+average(energies))/(k*T))
            if prob > random.random():
                energies.append(energy_two)
                states.append(sweeper)
        sweeper = state.copy()
    for i in states:
        mags.append(magnetization(i))
    data = []
    data.append(energies)
    data.append(mags)
    return data

def metropolis_sample(n=8, mu=1.1,k=1,J=-2,T=1, sweeps=100):
    """Computes the approximate values of average energy, average magnetization, heat capacity, and magnetic susceptibility of an arbitrary spin lattice of size n using the montecarlo simulation

    :param n: The size of the lattice, defaults to 8
    :type list: int
    :param mu: the magnetic constant, defualts to 1.1
    :type mu: float or int
    :param k: the boltzmann constant, defaults to 1
    :type k: float or int
    :param J: the ferromagnetic constant, defaults to -2
    :type J: float or int
    :param T: the temperature your state is in, defaults to 1
    :type T: float or int
    :param sweeps: The number of sweeps you'll take (more sweeps means more accurate simulation), defaults to 100
    :type sweeps: int
    :return: A list, the first item is the average energy, the second is the average magnetization, the third is the heat capacity, the fourth is the magnetic susceptibility
    :rtype: list
    """
    total_energies = []
    probabilities = []
    mags = []
    states = []
    for i in range(sweeps):
        tester_state = []
        for i in range(n):
            rand = random.random()
            if rand<.5:
                tester_state.append(-1)
            else:
                tester_state.append(1)
        states.append(tester_state)
        information = sweep(tester_state,mu,k,J,T)
        energies = information[0]
        magnet = information[1]
        for i in energies:
            total_energies.append(i)
        for i in magnet:
            mags.append(i)
    for i in range(len(total_energies)):
        probabilities.append(math.exp(-total_energies[i]/(k*T)))
    normalization = sum(probabilities)
    for i in range(len(probabilities)):
        probabilities[i] = probabilities[i]/normalization
    avg_eng = 0
    for i in range(len(total_energies)):
        avg_eng+=(total_energies[i]*probabilities[i])
    avg_mag = 0
    for i in range(len(mags)):
        avg_mag+=(mags[i]*probabilities[i])
    square_eng = total_energies.copy()
    for i in range(len(square_eng)):
        square_eng[i]=(square_eng[i]*square_eng[i])
    avg_square_eng =0
    for i in range(len(square_eng)):
        avg_square_eng+=(square_eng[i]*probabilities[i])
    heat_cap = (avg_square_eng - (avg_eng**2))/(k*T*T)
    
    square_mag = mags.copy()
    for i in range(len(square_mag)):
        square_mag[i]=(square_mag[i]*square_mag[i])
    avg_square_mag =0
    for i in range(len(square_mag)):
        avg_square_mag+=(square_mag[i]*probabilities[i])
    mag_sus = (avg_square_mag - (avg_mag**2))/(k*T)
    
    data = []
    data.append(avg_eng)
    data.append(avg_mag)
    data.append(heat_cap)
    data.append(mag_sus)
    return data



def metro_plot(tmin=1,tmax=10,step=0.1,J = -2, mu = 1.1, k = 1, n=8,sweeps=1000):
    """Plots average energy, average magnetization, heat capacity, and magnetic susceptibility with respect to varying temepratures using montecarlo simulations

    :param tmin: The lower temperature bound, defaults to 1
    :type tmin: float
    :param tmax: The upper temperature bound, defaults to 10
    :type tmax: float
    :param step: The number of increments between tmin and tmax
    :type step: float
    :param J: the ferromagnetic constant, defaults to -2
    :type J: float or int
    :param mu: the magnetic constant, defualts to 1.1
    :type mu: float or int
    :param k: the boltzmann constant, defaults to 1
    :type k: float or int
    :param n: the size of the spin lattice
    :type n: int
    :param sweeps: The number of sweeps you'll take (more sweeps means more accurate simulation), defaults to 100
    :type sweeps: int
    """
    temps = []
    average_energy = []
    average_magnetization = []
    heat_cap = []
    mag_sus = []
    for i in range(int((tmax-tmin)/step)):
        temps.append(tmin+i*step)
        data = metropolis_sample(n,mu,k,J,temps[-1],sweeps)
        average_energy.append(data[0])
        average_magnetization.append(data[1])
        heat_cap.append(data[2])
        mag_sus.append(data[3])
    plt.plot(temps,average_energy,'r-',temps,average_magnetization,'b-',temps,heat_cap,'g-',temps,mag_sus,'y-')
    plt.legend(["Average Energy", "Average Magnetization", "Heat Capacity", "Magnetic Susceptibility"],loc='best')
    plt.xlabel("Temperature (K)")
    plt.show()






