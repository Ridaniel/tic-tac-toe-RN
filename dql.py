# Red Neuronal Back-Propagation

import math
import random
import string
import numpy as np

# La funcion sigmoide 
def sigmoid(x):
    return 1/(1+math.e**(-x))

# La derivada de la funcion sigmoide en terminos de la salida (y)
def dsigmoid(y):
    return 1.0*y - y**2

class NN:
    def __init__(self, ni, nh, no):
        # Cantidad de nodos de las capas de entrada, oculta y salida
        self.ni = ni + 1 # +1 para el nodo de bias
        self.nh = nh 
        self.no = no

        # Activaciones para los nodos
        self.ai = [0.0]*self.ni
        self.ah = [0.0]*self.nh
        self.ao = [0.0]*self.no
        
        # Se crea las matrices de pesos 
        self.wi = np.zeros((self.ni, self.nh))
        self.wo = np.zeros((self.nh, self.no))

        # Ultimo cambio en los pesos por el factor de inercia
        self.ci = np.zeros((self.ni, self.nh))
        self.co = np.zeros((self.nh, self.no))


    def update(self, obs, simbol,weight):
        for i in range(0,self.ni-2):
            self.ai[i] = obs[int(i/weight)][int(i%weight)]+1
        self.ai[self.ni-1]=simbol+1

        # Activaciones de oculta
        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):    
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = sigmoid(sum)

        # Activaciones de salida
        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k]=sum

        return self.ao[:]


    def backPropagate(self,action,value, N, M):
        assert action<self.no, "Acción no valida pues "

        # Calcula el error para la capa de salida
        output_deltas = 0
        error = value-self.ao[action]
        output_deltas = dsigmoid(self.ao[action]) * error

        # Calcula el error para la capa oculta 
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            error = error + output_deltas*self.wo[j][action]
            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        # Actualiza los pesos de oculta-salida
        for j in range(self.nh):
                change = output_deltas*self.ah[j]
                self.wo[j][action] = self.wo[j][action] + N*change + M*self.co[j][action]
                self.co[j][action] = change
                #print N*change, M*self.co[j][k]

        # Actualiza los pesos de entrada-oculta
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
                self.ci[i][j] = change

        # Calcula el error
        error = 0.0
        error = error + 0.5*(value-self.ao[action])**2
        return error

    def weights(self):
        print('Pesos de Entrada:')
        for i in range(self.ni):
            print(self.wi[i])
        print()
        print('Pesos de Salida:')
        for j in range(self.nh):
            print(self.wo[j])

    def output(self):
        return self.ao
    
    def max(self):
        action=0
        for i in range(self.no):
            if(self.ao[i]>self.ao[action]):
                i=action
        return action

    def next(self,obs,simbol1,simbol2,weight):
        qtemp=self
        qtemp.update(obs.tablero,simbol2,weight)
        r=qtemp.max()
        return qtemp.ao[r]
    
