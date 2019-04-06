from SwallowQLearner import train

print("Ingrese el número de pruebas para entrenar la RN: ")
test = int(input())
print("Ingrese el número de filas para el tablero: ")
rows = int(input())
print("Ingrese el número de columna para el tablero: ")
columns = int(input())
train(test, int(rows*columns/2)+1, rows, columns)
