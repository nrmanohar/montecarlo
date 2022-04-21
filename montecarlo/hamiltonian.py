"""Provide the primary functions."""
import numpy as np
import matplotlib.pyplot as plt
plt.clf()
plt.cla()
plt.close()
class Hamiltonian:
    '''
    This is a simple class to calculate the hamiltonian for a spin configuration

    :param J: The ferromagnetic constant for the material, defaults to -2
    :type J: int, optional

    :param mu: magnetic constant for energy calcualation, defaults to 1.1
    :type mu: int, optional

    :param k: The Boltzmann constant, defaults to 1
    :type k: float, optional
    
    :param state: The state that is being analyzed, defaults to [1,-1,1,-1]
    :type state: list, optional 
    '''
    def __init__(self,J = -2,mu=1.1,k=1,state=[1,-1,1,-1]):
        """Constructor method

        """
        self.energy = 0
        self.state = state
        self.j = J
        self.mu = mu
        self.k = k
    def initialize(self,list):
        """Initializes itself using a list. Note, all lists should be in the format of a sequential list where 1 is spin up and -1 is spin down

        :param list: A list of spin orientations
        :type list: list
        """
        for i in list:
            self.state.append(i)
    def reset(self):
        """Resets the object to default settings

        """
        self.state.clear()
        self.energy = 0
    def spin_energy(self):
        """Calculates the spin energy using the Ising model

        :rtype: float 
        """
        for i in range(len(self.state)-1):
            self.energy+=(self.state[i]*self.state[i+1])
        self.energy+=self.state[0]*self.state[-1]
        self.energy*= -self.j/self.k
    
        for j in self.state:
            self.energy+=(self.mu*j)    
        return self.energy

def magnetization(spin_config):
    """Computes the magnetization alone of some spin configuration. Note, all lists should be in the format of a sequential list where 1 is spin up and -1 is spin down

    :param spin_config: A list of spin orientations
    :type list: list
    :return: The computed magnetization for a spin configuration of listed spin states
    :rtype: int
    """
    magnet = 0
    for i in spin_config:
        magnet+=i
    return magnet

class spin_config_1D:
    '''
    This is a simple class to calculate the energy distribution for all configurations of size n

    :param boltz: The boltzmann constant for your calculations, defaults to 1
    :type boltz: int or float

    :param J: The ferromagnetic constant for your calculations, defaults to -2
    :type J: int or float

    :param mu: The magnetization constant for your calculations, defaults to 1.1
    :type mu: int or float

    :param temp: The temperature your spin lattice is held in (in kelvin), defaults to 373K (100 degrees Celsius)
    :type temp: int or float

    :param n: The size of lattice you're testing
    :type n: int
    '''
    def __init__(self,boltz=1,J=-2,mu=1.1,temp=373,n=8):
        self.energies = []
        self.size = n
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
        self.calc(self.size)
    def calc(self,n):
        """Calculates the energies for all configurations of size n and puts them in an array, along with average energy, average magnetization, heat capacity, and magnetic susceptibility, along with the probabilities, and all the states

        :param n: The number of sites on the spin configurations that you want to test
        :type n: int
        """
        self.generate_state(n)
        #Generates the states
        self.energy_generation()       
        #Generates the energies of each state    
        self.magnetic_generation()
        #Generates the magnetizations of each state    
        self.boltzmann_distribution()
        #Generates the boltzmann distribution
        self.probabilities_generation()
        #Generates the probabiliites, now normalized
        self.averages()
        #Computes average energy and magnetization
        self.heat_capacity_calculator()
        #Computes heat capacity
        self.magnetic_sus_calculator()
        #Computes magnetic suscpetibility        
    def reset(self):
        """Resets the configuration to all default values and default constants
        
        """
        self.energies = []
        self.size = 8
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
        """Resets the configuration to all default values but maintains the constants
        
        """
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
        """Modifies the temperature alone
        
        :param temp: The temperature you want to set your state at
        """
        self.T = temp
        self.calc(self.size)
    def J(self,pref):
        """Modifies the ferromagnetic preference alone
        
        :param pref: The J value do you want to set your state at
        """
        self.j = pref
        self.calc(self.size)
    def boltz(self,k):
        """Modifies the boltzmann constant alone
        
        :param k: The k value do you want to set your state at
        """
        self.k = boltz
        self.calc(self.size)
    def mu(self,mu):
        """Modifies the magnetic preference alone
        
        :param mu: The mu value do you want to set your state at
        """
        self.mu = mu
        self.calc(self.size)
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

    def __str__(self):
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
        """Modifies the all the constants together
        
        :param boltz: Set your boltzmann constant at
        :param pref: Set your ferromagnetic preferentiabiility
        :param mu: Set your magnetic constant
        :param temp: Set your temperature 
        """
        self.k = boltz
        self.j = pref
        self.mu = mu
        self.T = temp
    def energy_generation(self):
        """Takes all states and calculates the energy in each states and stores it in a list
        
        """
        for j in self.states:
            energy = 0
            for i in range(len(j)-1):
                energy+=(j[i]*j[i+1])
            energy+=j[-1]*j[0]
            energy *= -self.j/self.k
            for k in j:
                energy+=(self.mu*k)
            self.energies.append(energy)
    def magnetic_generation(self):
        """Takes all states and calculates the magentization and stores it in a list
        
        """
        for j in self.states:
            magnet = 0
            for i in j:
                magnet+=i
            self.magnetizations.append(magnet)
    def boltzmann_distribution(self):
        """Calculates the unnormalized probability distribution using each state's energy
        
        """
        for i in self.energies:
            self.boltzmann.append(np.exp(-i/(self.k*self.T)))
    def probabilities_generation(self):
        """Takes the boltzmann distribution and normalizes it
        
        """
        norm = sum(self.boltzmann)
        for j in range(len(self.boltzmann)):
            self.probabilities.append(self.boltzmann[j]/norm)
    def averages(self):
        """Computes weighted average energy and magnetization using the energy and probabilities list
        
        """
        for i in range(len(self.energies)):
            self.avg_eng+=self.energies[i]*self.probabilities[i]
        for i in range(len(self.magnetizations)):
            self.avg_mag+=self.magnetizations[i]*self.probabilities[i]
    def heat_capacity_calculator(self):
        """Calculates the heat capacity using the calculation based on the energies
        
        """
        copy_energy=[]
        E = 0     
        for i in self.energies:
            copy_energy.append(i**2)
        for i in range(len(copy_energy)):
            E+=copy_energy[i]*self.probabilities[i]
        self.heat_capacity = (E - np.power(self.avg_eng,2))/(self.k*self.T*self.T) 
    def magnetic_sus_calculator(self):
        """Calculates the magnetic susceptibility using the calculation based on the energies
        
        """
        copy_mag=[]
        M = 0
        for i in range(len(self.magnetizations)):
            copy_mag.append(self.magnetizations[i]**2)
        for i in range(len(copy_mag)):
            M+=copy_mag[i]*self.probabilities[i]
        self.mag_sus = (M - np.power(self.avg_mag,2))/(self.k*self.T)
    def generate_state(self,n=8):
        """Generates every possible lattice state for n lattice sites

        :param n: Size of the lattice
        :type n: int        
        """
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
    def generate_plot(self,tmin=1,tmax=10,step=0.1,J = -2, mu = 1.1, k = 1, num_states=8):
        """
        Generates the plot for average energy, average magnetizatoin, heat capacity, and magnetic susceptibility over various temperatures.

        :param tmin: minimum temperature, defaults to 1K
        :type tmin: float
        :param tmax: max temperature, defaults to 10K
        :type tmax: float
        :param step: Every interval over which a datapoint is measured, defaults to a step of 0.1
        :type step: float
        :param J: Ferromagnetic constant, defaults to -2
        :type J: int or float
        :param mu: Magnetization constant, defaults to 1.1
        :type mu: int or float
        :param k: Boltzmann constant
        :type k: int or float
        :param num_states: The number of states in the lattice
        :type num_states: int
        """
        t_current = self.T
        temps = []
        average_energy = []
        average_magnetization=[]
        heat_cap=[]
        mag_sus=[]
        for i in range(int(tmin),int((tmax-tmin)/step)):
            temps.append(tmin+i*step)
            self.constants(k,J,mu,tmin+i*step)
            self.calc(num_states)
            average_energy.append(self.avg_eng)
            average_magnetization.append(self.avg_mag)
            heat_cap.append(self.heat_capacity)
            mag_sus.append(self.mag_sus)
        plt.plot(temps,average_energy,'r-',temps,average_magnetization,'b-',temps,heat_cap,'g-',temps,mag_sus,'y-')
        plt.legend(["Average Energy", "Average Magnetization", "Heat Capacity", "Magnetic Susceptibility"],loc='best')
        plt.xlabel("Temperature (K)")
        plt.show()
        self.T = t_current
        
        
if __name__ == "__main__":
    # Do something if this file is invoked on its own
    generator = spin_lattice_1D(n=2)
    print(generator)
