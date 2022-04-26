from .hamiltonian import *
import numpy as np
import matplotlib.pyplot as plt
plt.clf()
plt.cla()
plt.close()
import random
import math

def average(list):
    sum=0
    for i in list:
        sum+=i
    return sum/len(list)

def sweep(state, mu=1.1, k=1, J=-2, T=1):
    energies = []
    energies.append(spin_energy(J,mu,k,state))
    sweeper = state.copy()
    for i in range(len(sweeper)):
        if sweeper[i]==-1:
            sweeper[i]=1
        elif sweeper[i]==1:
            sweeper[i]==-1
        energy_two = spin_energy(J,mu,k,sweeper)
        if energy_two < energies[0]:
            energies.append(energy_two)
        else:
            prob = math.exp(-energy_two/(k*T))
            if prob>random.random():
                energies.append(energy_two)
        sweeper = state.copy()
    return energies
def metropolis_sample_energy(n=8, mu=1.1,k=1,J=-2,T=1, sweeps=100):
    total_energies = []
    for i in range(sweeps):
        tester_state = []
        for i in range(n):
            rand = random.random()
            if rand<.5:
                tester_state.append(-1)
            else:
                tester_state.append(1)
        energies = sweep(tester_state,mu,k,J,T)
        for i in energies:
            total_energies.append(i)
    return total_energies

def plot(tmin=1,tmax=10,step=0.1,J = -2, mu = 1.1, k = 1, num_states=8,sweeps=1000):
    temps = []
    average_energy = []
    for i in range(int(tmin),int((tmax-tmin)/step)):
        temps.append(tmin+i*step)
        energies = metropolis_sample_energy(num_states,mu,k,J,temps[-1],sweeps)
        average_energy.append(average(energies))
    plt.plot(temps,average_energy)
    plt.legend(["Average Energy"],loc='best')
    plt.xlabel("Temperature (K)")
    plt.show()






