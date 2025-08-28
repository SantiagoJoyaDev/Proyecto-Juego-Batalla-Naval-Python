import random # Importamos la libreria random para generar numeros 
#aleatorios que generan las coordenanas aleatorias
import os
import pygame # Importamos la libreria pygame par los sonidos (Solo se esta usando
# para los sonidos)
pygame.init() # Inicializamos pygame
pygame.mixer.init() # Inicializamos el modulo de sonido de pygame

sonido_disparo_acertado = pygame.mixer.Sound("Acertado.wav") # Cargamos el sonido de disparo acertado
sonido_disparo_fallado = pygame.mixer.Sound("Fallado.wav") # Cargamos el sonido de disparo fallado

# Definimos las dimensiones del tablero
filas = 10 # Definimos el numero de filas del tablero
columnas = 10 # Definimos el numero de columnas del tablero
mar = " " # Definimos el espacio vacio que es el mar

#Definimos los barcos que hay en el juego
submarino = "S" #Ocupa 1 celda
crucero = "C" #Ocupa 2 celdas
destructor = "D" #Ocupa 3 celdas
acorazado = "A" #Ocupa 4 celdas

#definimos los simbolos de los disparos
disparo_acertado = "O" #Simbolo de disparo acertado
disparo_fallado = "X" #Simbolo de disparo fallado

# Definimos la cantiddad de disparos que tiene el jugador
disparos_totales = 30 # El jugador tiene 30 disparos para hundir todos los barcos

#definimos la cantidad de barcos iniciales
cantidad_submarinos = 4 # El jugador tiene 4 submarinos
cantidad_cruceros = 3 # El jugador tiene 3 cruceros
cantidad_destructores = 2 # El jugador tiene 2 destructores
cantidad_acorazados = 1 # El jugador tiene 1 acorazado

#definimos los tipos de jugadores
jugador1 = "J1"
jugador2 = "J2"
maquina = "M"














print("!!!!!BIENVENIDO A EL JUEGO DE BATALLA NAVAL!!!!!")
