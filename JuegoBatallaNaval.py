import random
import os
import pygame

# Inicialización de Pygame para los sonidos
pygame.init()
pygame.mixer.init()

sonido_disparo_acertado = pygame.mixer.Sound("sonidos/Acertado.wav")
sonido_disparo_fallado = pygame.mixer.Sound("sonidos/Fallido.wav")

# Dimensiones del tablero
filas = 6
columnas = 6
mar = " "

# Tipos de barcos
submarino = "S"  # 1 celda
crucero = "C"    # 2 celdas
destructor = "D" # 3 celdas
acorazado = "A"  # 4 celdas

# Disparos
disparo_acertado = "O"
disparo_fallado = "X"
disparos_totales = 30

# Cantidades de barcos
cantidad_submarinos = 4
cantidad_cruceros = 3
cantidad_destructores = 2
cantidad_acorazados = 1

# Jugadores
jugador1 = "J1"
jugador2 = "J2"
maquina = "M"

print("!!!!!BIENVENIDO A EL JUEGO DE BATALLA NAVAL!!!!!")
print("!!!!!BY SANTIAGO JOYA!!!!!")

def obtener_matriz_inicial():
    matriz = []
    for y in range(filas):
        matriz.append([mar] * columnas)
    return matriz

def letras(letra):
    return chr(ord(letra) + 1)

def imprimir_separador_vertical():
    for _ in range(columnas + 1):
        print("+-----", end="")
    print("+")

def separador_numeros():
    print("|     ", end="")
    for x in range(columnas):
        print(f"|  {x+1}  ", end="")
    print("|")

def coordenada_vacia(x, y, matriz):
    return matriz[y][x] == mar

def coordenada_en_rango(x, y):
    return 0 <= x < columnas and 0 <= y < filas

def obtener_x_aleatorio():
    return random.randint(0, columnas - 1)

def obtener_y_aleatorio():
    return random.randint(0, filas - 1)

def colocar_barco(matriz, longitud, tipo_barco, cantidad):
    barcos_colocados = 0
    intentos_max = 1000  # límite de intentos para evitar bucles infinitos
    intentos = 0

    while barcos_colocados < cantidad and intentos < intentos_max:
        intentos += 1
        x = obtener_x_aleatorio()
        y = obtener_y_aleatorio()
        orientacion = random.choice(["H", "V"])

        if orientacion == "H" and x + longitud - 1 < columnas:
            if all(coordenada_vacia(x+i, y, matriz) for i in range(longitud)):
                for i in range(longitud):
                    matriz[y][x+i] = tipo_barco
                barcos_colocados += 1

        elif orientacion == "V" and y + longitud - 1 < filas:
            if all(coordenada_vacia(x, y+i, matriz) for i in range(longitud)):
                for i in range(longitud):
                    matriz[y+i][x] = tipo_barco
                barcos_colocados += 1

    return matriz

def colocar_todos_los_barcos(matriz):
    matriz = colocar_barco(matriz, 1, submarino, cantidad_submarinos)
    matriz = colocar_barco(matriz, 2, crucero, cantidad_cruceros)
    matriz = colocar_barco(matriz, 3, destructor, cantidad_destructores)
    matriz = colocar_barco(matriz, 4, acorazado, cantidad_acorazados)
    return matriz

# Crear matriz inicial y colocar los barcos
tablero = obtener_matriz_inicial()
tablero = colocar_todos_los_barcos(tablero)

# Imprimir tablero (solo para pruebas, esto normalmente estaría oculto)
for fila in tablero:
    print(fila)
