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
        square_eng[i]=(square_mag[i]*square_mag[i])
    avg_square_mag =0
    for i in range(len(square_mag)):
        avg_square_mag+=(square_mag[i]*probabilities[i])
    mag_sus = -(avg_square_mag - (avg_mag**2))/(k*T)
    
    data = []
    data.append(avg_eng)
    data.append(avg_mag)
    data.append(heat_cap)
    data.append(mag_sus)
    return data



def metro_plot(tmin=1,tmax=10,step=0.1,J = -2, mu = 1.1, k = 1, num_states=8,sweeps=1000):
    temps = []
    average_energy = []
    average_magnetization = []
    heat_cap = []
    mag_sus = []
    for i in range(int(tmin),int((tmax-tmin)/step)):
        temps.append(tmin+i*step)
        data = metropolis_sample(num_states,mu,k,J,temps[-1],sweeps)
        average_energy.append(data[0])
        average_magnetization.append(data[1])
        heat_cap.append(data[2])
        mag_sus.append(data[3])
    plt.plot(temps,average_energy,'r-',temps,average_magnetization,'b-',temps,heat_cap,'g-',temps,mag_sus,'y-')
    plt.legend(["Average Energy", "Average Magnetization", "Heat Capacity", "Magnetic Susceptibility"],loc='best')
    plt.xlabel("Temperature (K)")
    plt.show()






