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
    def __init__(self, ni, nh, no, co=1):
        # Cantidad de nodos de las capas de entrada, oculta y salida
        self.ni = ni + 1  # +1 para el nodo de bias
        self.co = co
        self.nh = nh
        self.no = no

        # Activaciones para los nodos
        self.ai = [0.0]*self.ni
        self.ah = np.zeros((self.co, self.nh))
        self.ao = [0.0]*self.no

        # Se crea las matrices de pesos
        self.wi = np.zeros((self.ni, self.nh))
        self.wco = np.zeros((self.co-1, self.nh, self.nh))
        self.wo = np.zeros((self.nh, self.no))

        # Ultimo cambio en los pesos por el factor de inercia
        self.ci = np.zeros((self.ni, self.nh))
        self.cco = np.zeros((co-1, self.nh, self.nh))
        self.coo = np.zeros((self.nh, self.no))

    def update(self, board, simbol):
        for i in range(0, self.ni-2):
            self.ai[i] = board[int(i/len(board[0]))][int(i % len(board[0]))]+1
        self.ai[self.ni-1] = simbol+1

        # Activaciones de las capas oculta
        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[0][j] = sigmoid(sum)

        for k in range(0, int(self.co-1)):
            for j in range(self.nh):
                sum = 0.0
                for i in range(self.nh):
                    sum = sum + self.ah[k][i]*self.wco[k][i][j]
                self.ah[k+1][j] = sigmoid(sum)

        # Activaciones de salida
        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum = sum + self.ah[self.co-1][j] * self.wo[j][k]
            self.ao[k] = sum

        return self.ao[:]

    def backPropagate(self, action, value, N, M):
        assert action < self.no, "Acción no valida pues "

        # Calcula el error para la capa de salida
        output_deltas = 0
        error = value-self.ao[action]
        output_deltas = dsigmoid(self.ao[action]) * error

        # Calcula el error para la capa oculta
        hidden_deltas = np.zeros((self.co, self.nh))
        for j in range(self.nh):
            error = 0.0
            error = error + output_deltas*self.wo[j][action]
            hidden_deltas[self.co -
                          1][j] = dsigmoid(self.ah[self.co-1][j]) * error

        for i in range(self.co-2, 0, -1):
            for k in range(self.nh):
                error = 0.0
                for j in range(self.nh):
                    error = error + hidden_deltas[i+1][j]*self.wco[i][k][j]
                hidden_deltas[i][k] = dsigmoid(self.ah[i][j]) * error

        # Actualiza los pesos de oculta-salida
        for j in range(self.nh):
            change = output_deltas*self.ah[self.co-1][j]
            self.wo[j][action] = self.wo[j][action] + \
                N*change + M*self.coo[j][action]
            self.coo[j][action] = change
            # print N*change, M*self.co[j][k]

        # actualiza los pesos oculta-oculta
        for i in range(self.co-2, 0, -1):
            for j in range(self.nh):
                for k in range(self.nh):
                    change = hidden_deltas[i+1][j]*self.ah[i][k]
                    self.wco[i][k][j] = self.wco[i][k][j] + \
                        N*change + M*self.cco[i][k][j]
                    self.cco[i][k][j] = change

        # Actualiza los pesos de entrada-oculta
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[0][j]*self.ai[i]
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
        action = 0
        for i in range(self.no):
            if(self.ao[i] > self.ao[action]):
                i = action
        return action

    def next(self, obs, simbol1, simbol2):
        qtemp = self
        qtemp.update(obs.tablero, simbol2)
        r = qtemp.max()
        return qtemp.ao[r]
