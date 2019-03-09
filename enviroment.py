import numpy as np
import copy


class enviroments():
    def __init__(self, height, widht):
        self.tablero = np.zeros((height, widht), int)
        self.height = height
        self.widht = widht
        self.reward = 0
        self.done = False
        self.jugadas = 0    
        self.puntajes = [0, 0]

    def update(self, action, simbolo):
        """
        :action:    Es la acción que se plantea realizar
        :simbolo:   Es el simbolo que identifica al jugador
        """
        #Se hace una copia de estado del juego antes de la jugada propuesta
        enviromentTemp = copy.deepcopy(self)
        #Se verifica que la jugada no sea ilegal
        if(action >= self.height*self.widht or self.tablero[int(action/self.widht)][int(action % self.widht)] != 0):
            enviromentTemp.reward = -25
        else:
            enviromentTemp.jugadas += 1

            if(enviromentTemp.jugadas == enviromentTemp.height*enviromentTemp.widht):
                enviromentTemp.done = True
            enviromentTemp.tablero[int(
                action/self.widht)][int(action % self.widht)] = simbolo
            enviromentTemp.reward = enviromentTemp.rewards(action, simbolo)

        #Se devuelve el nuevo estado del juego
        return enviromentTemp

    def rewards(self, action, simbolo):
        reward = 5
        for i in range(int(action/self.widht)-2, int(action/self.widht)):
            for j in range(int(action % self.widht)-2, int(action % self.widht)):
                if(i < 0 or j < 0 or self.tablero[i][j] != simbolo):
                    break
                if(-int(action/self.widht)+i-j+int(action % self.widht) == 0 and i+2 < self.height and j+2 < self.widht):
                    if(self.tablero[i+1][j+1] == simbolo and self.tablero[i+2][j+2] == simbolo):
                        reward += 10
                if(int(action % self.widht)-j == 0 and i+2 < self.height):
                    if(self.tablero[i+1][j] == simbolo and self.tablero[i+2][j] == simbolo):
                        reward += 10
                if(int(action % self.widht)-i == 0 and j+2 < self.widht):
                    if(self.tablero[i][j+1] == simbolo and self.tablero[i][j+2] == simbolo):
                        reward += 10
        self.puntajes[simbolo-1] += int((reward-5)/10)
        return reward

    def final(self, simbol):
        for i in self.puntajes:
            if(self.puntajes[simbol-1] < i and i != simbol-1):
                return 0*len(self.tablero)*len(self.tablero[0])

            if(self.puntajes[simbol-1] == i and i != simbol-1):
                return 10*len(self.tablero)*len(self.tablero[0])
        return 10*len(self.tablero)*len(self.tablero[0])


