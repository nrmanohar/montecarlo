"""Provide the primary functions."""

import numpy as np
import matplotlib.pyplot as plt

def canvas(with_attribution=True):
    """
    Placeholder function to show example docstring (NumPy format).

    Replace this function and doc string for your own project.

    Parameters
    ----------
    with_attribution : bool, Optional, default: True
        Set whether or not to display who the quote is from.

    Returns
    -------
    quote : str
        Compiled string including quote and optional attribution.
    """

    quote = "The code is but a canvas to our imagination."
    if with_attribution:
        quote += "\n\t- Adapted from Henry David Thoreau"
    return quote

class Hamiltonian:
    def __init__(self,J = -2,mu=1.1,k=1,state=[]):
        self.energy = 0
        self.state = state
        self.j = J
        self.mu = mu
        self.k = k
    def initialize(self,list):
        for i in list:
            self.state.append(i)
    def reset(self):
        self.state.clear()
        self.energy = 0
    def spin_energy(self):
        for i in range(len(self.state)-1):
            self.energy+=(self.state[i]*self.state[i+1])
        self.energy+=self.state[0]*self.state[-1]
        self.energy*= -self.j/self.k
    
        for j in self.state:
            self.energy+=(self.mu*j)    
        return self.energy

def magnetization(spin_config):
    magnet = 0
    for i in spin_config:
        magnet+=i
    return magnet

class spin_config_1D:
    def __init__(self,boltz=1,J=-2,mu=1.1,temp=373,n=8):
        self.energies = []
        self.magnetizations = []
        self.probabilities = []
        self.boltzmann = []
        self.states = []
        self.k = boltz
        self.j = J
        self.mu = mu
        self.T = temp
        self.avg_eng = 0
        self.avg_mag = 0
        self.heat_capacity = 0
        self.mag_sus = 0
        self.generate_state(n)
    def reset(self):
        self.energies = []
        self.magnetizations = []
        self.probabilities = []
        self.boltzmann = []
        self.states = []
        self.k = 1
        self.j = -2
        self.mu = 1.1
        self.T = 323
        self.avg_eng = 0
        self.avg_mag = 0
        self.heat_capacity = 0
        self.mag_sus = 0
    def clean(self):
        self.energies = []
        self.magnetizations = []
        self.probabilities = []
        self.boltzmann = []
        self.states = []
        self.avg_eng = 0
        self.avg_mag = 0
        self.heat_capacity = 0
        self.mag_sus = 0
    def temp(self,temp):
        self.T = temp
    def J(self,pref):
        self.j = pref
    def boltz(self,k):
        self.k = boltz
    def mu(self,m):
        self.mu = m
    def __repr__(self):
        string = "States: "+str(self.states)+'\n'
        string+="Energies: "+str(self.energies)+'\n'
        string+="Magnetizations: "+str(self.magnetizations)+'\n'
        string+="Probabilities: "+str(self.probabilities)+'\n'
        string+="Average Energy: "+str(self.avg_eng)+'\n'
        string+="Average Magnetization: "+str(self.avg_mag)+'\n'
        string+="Heat Capcity: "+str(self.heat_capacity)+'\n'
        string+="Magnetic Susceptibility: "+str(self.heat_capacity)+'\n'
        string+="Constants\n"
        string+="\tBoltzmann Constant is: "+str(self.k)+'\n'
        string+="\tJ is: "+str(self.j)+'\n'
        string+="\tmu is: "+str(self.mu)+'\n'
        string+="\tTemperature is: "+str(self.T)
        return string
        
    def constants(self,boltz,pref,mu,temp):
        self.k = boltz
        self.j = pref
        self.mu = mu
        self.T = temp
    def generate_state(self,n=8):
        self.clean()
        for i in range(2**n):
            binary = bin(i)
            state = [char for char in binary]
            state.remove('0')
            state.remove('b')
            for j in range(len(state)):
                state[j] = int(state[j])
                if state[j]==0:
                    state[j]=-1
            while len(state)<n:
                state.insert(0,-1)
            self.states.append(state)
        #Generates the states
        
        for j in self.states:
            energy = 0
            for i in range(len(j)-1):
                energy+=(j[i]*j[i+1])
            energy+=j[-1]*j[0]
            energy *= -self.j/self.k
            for k in j:
                energy+=(self.mu*k)
            self.energies.append(energy)
        #Generates the energies of each state    
        
        for j in self.states:
            magnet = 0
            for i in j:
                magnet+=i
            self.magnetizations.append(magnet)
        #Generates the magnetizations of each state    
        
        for i in self.energies:
            self.boltzmann.append(np.exp(-i/(self.k*self.T)))
        normalization_factor = sum(self.boltzmann)
        
        #Generates the probability graph, unnormalized as a list
        
        for j in range(len(self.boltzmann)):
            self.probabilities.append(self.boltzmann[j]/normalization_factor)
            
        #Generates a new list, normalized this time
        
        for i in range(len(self.energies)):
            self.avg_eng+=self.energies[i]*self.boltzmann[i]
        self.avg_eng/=normalization_factor
        
        #Computes average energy
        for i in range(len(self.magnetizations)):
            self.avg_mag+=self.magnetizations[i]*self.boltzmann[i]
        self.avg_mag/=normalization_factor
        
        #Computes average magnetization
        
        copy_energy=[]
        E = 0        
        for i in self.energies:
            copy_energy.append(i**2)
        for i in range(len(copy_energy)):
            E+=copy_energy[i]*self.boltzmann[i]
        E/=normalization_factor
        self.heat_capacity = (E - np.power(self.avg_eng,2))/(self.k*self.T*self.T)
        
        #Computes heat capacity
        
        copy_mag=[]
        M = 0        
        for i in range(len(self.magnetizations)):
            copy_mag.append(self.magnetizations[i]**2)
        for i in range(len(copy_mag)):
            M+=copy_mag[i]*self.boltzmann[i]
        M/=normalization_factor
        self.mag_sus = (M - np.power(self.avg_mag,2))/(self.k*self.T)
        
        #Computes magnetic suscpetibility
        
    def generate_plot(self,tmin=1,tmax=10,step=0.1,num_states=8):
        t_current = self.T
        temps = []
        average_energy = []
        average_magnetization=[]
        heat_cap=[]
        mag_sus=[]
        for i in range(int(tmin),int(tmax/step)):
            temps.append(i*step)
            self.temp(i*step)
            self.generate_state(num_states)
            average_energy.append(self.avg_eng)
            average_magnetization.append(self.avg_mag)
            heat_cap.append(self.heat_capacity)
            mag_sus.append(self.mag_sus)
        plt.plot(temps,average_energy,'r-',temps,average_magnetization,'b-',temps,heat_cap,'g-',temps,mag_sus,'y-')
        plt.legend(["Average Energy", "Average Magnetization", "Heat Capacity", "Magnetic Susceptibility"],loc='best')
        plt.xlabel("Temperature (K)")
        self.T = t_current


if __name__ == "__main__":
    # Do something if this file is invoked on its own
    print(canvas())
