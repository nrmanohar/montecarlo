def spin_energy(list, J = -2, mu = 1.1, k = 1):
        energy = 0
        for i in range(len(list)-1):
            energy+=(list[i]*list[i+1])
        energy+=state[0]*state[-1]
        energy*= -J/k
    
        for j in list:
            energy+=(mu*j)    
        return energy


def metropolis_sweep(list):
    pass
    
