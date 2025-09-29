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

# ---------------- FUNCIONES BÁSICAS ---------------- #

def obtener_matriz_inicial():
    matriz = []
    for y in range(filas):
        matriz.append([mar] * columnas)
    return matriz

def letras(letra):
    return chr(ord(letra) + 1) #El chr es para convertir a caracter y ord para convertir a numero

def imprimir_separador_vertical(): #Separador vertical
    for _ in range(columnas + 1):
        print("+-----", end="")
    print("+")

def separador_numeros(): #Separador horizontal
    print("|     ", end="")
    for x in range(columnas):
        print(f"|  {x+1}  ", end="")
    print("|")

def coordenada_vacia(x, y, matriz):
    return matriz[y][x] == mar

def coordenada_en_rango(x, y):
    return x >= 0 and x <= columnas-1 and y >= 0 and y <= filas-1

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
        orientacion = random.choice(["H", "V"]) # Aqui se elige si el barco va horizontal o vertical (H o V) el choice es para 
        #elegir entre dos opciones

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

def imprimir_tablero_oculto(matriz):
    imprimir_separador_vertical()
    separador_numeros()
    imprimir_separador_vertical()

    for y in range(filas):
        print(f"|  {chr(ord('A') + y)}  ", end="")  # Etiqueta de fila (A, B, C...)
        for x in range(columnas):
            if matriz[y][x] in [disparo_acertado, disparo_fallado]:
                print(f"|  {matriz[y][x]}  ", end="")
            else:
                print(f"|     ", end="")  # No muestra los barcos
        print("|")
        imprimir_separador_vertical()
        
# ===================== FUNCIONES VISUALIZACIÓN =====================

def imprimir_tablero(tablero, oculto=False):
    """
    Imprime el tablero con estilo de matriz (celdas y separadores)
    Si oculto=True, se ocultan los barcos (solo se ven disparos O/X).
    """
    # Separador superior con números de columna
    imprimir_separador_vertical()
    print("|     ", end="")
    for col in range(columnas):
        print(f"|  {col+1}  ", end="")
    print("|")
    imprimir_separador_vertical()

    for y in range(filas):
        print(f"|  {chr(ord('A') + y)}  ", end="")  # Etiqueta de fila (A, B, C...)
        for x in range(columnas):
            celda = tablero[y][x]
            if oculto and celda in [submarino, crucero, destructor, acorazado]:
                mostrar = mar
            elif celda == mar:
                mostrar = " "
            else:
                mostrar = celda
            print(f"|  {mostrar}  ", end="")
        print("|")
        imprimir_separador_vertical()

# ---------------- FUNCIONES DE JUEGO ---------------- #

def pedir_coordenada(jugador, disparos_realizados):
    if jugador == maquina:
        while True:
            x = obtener_x_aleatorio()
            y = obtener_y_aleatorio()
            if (x, y) not in disparos_realizados:
                print(f"[{maquina}] dispara en {chr(ord('A')+y)}{x+1}")
                return x, y
    else:
        while True:
            entrada = input(f"{jugador}, ingresa tu disparo (ej: A3): ").upper().strip()
            if len(entrada) < 2:
                print(" Formato inválido. Usa letra+numero (ej: A3).")
                continue
            letra = entrada[0]
            numero = entrada[1:]
            if not numero.isdigit(): # Verifica que el número sea válido el insdigit es para verificar si es un numero
                print(" El número no es válido.")
                continue
            x = int(numero) - 1
            y = ord(letra) - ord("A")
            if not coordenada_en_rango(x, y):
                print(" Coordenada fuera de rango.")
                continue
            if (x, y) in disparos_realizados:
                print(" Ya disparaste en esa coordenada.")
                continue
            return x, y

def procesar_disparo(x, y, tablero, disparos_realizados):
    disparos_realizados.add((x, y))
    if tablero[y][x] in [submarino, crucero, destructor, acorazado]:
        tablero[y][x] = disparo_acertado
        sonido_disparo_acertado.play()
        return True
    else:
        tablero[y][x] = disparo_fallado
        sonido_disparo_fallado.play()
        return False

def contar_barcos_restantes(tablero):
    return {
        "Submarinos": sum(fila.count(submarino) for fila in tablero),
        "Cruceros": sum(fila.count(crucero) for fila in tablero),
        "Destructores": sum(fila.count(destructor) for fila in tablero),
        "Acorazados": sum(fila.count(acorazado) for fila in tablero),
    }
    
# ===================== FUNCIONES DE PARTIDA =====================

def jugar_j1_vs_j2():
    print("\n=== MODO: J1 vs J2 ===")
    tablero_j1 = colocar_todos_los_barcos(obtener_matriz_inicial())
    tablero_j2 = colocar_todos_los_barcos(obtener_matriz_inicial())
    disparos_j1, disparos_j2 = set(), set()
    disparos_restantes_j1, disparos_restantes_j2 = disparos_totales, disparos_totales
    turno = 1

    # Mostrar tableros iniciales (ocultos)
    print("\nTablero de J1 (oculto para J2):")
    imprimir_tablero(tablero_j1, oculto=True)
    print("\nTablero de J2 (oculto para J1):")
    imprimir_tablero(tablero_j2, oculto=True)

    while disparos_restantes_j1 > 0 and disparos_restantes_j2 > 0:
        print(f"\n===== RONDA {turno} =====")
        
        # Turno J1
        print("\nTurno de J1")
        x, y = pedir_coordenada(jugador1, disparos_j1)
        acierto = procesar_disparo(x, y, tablero_j2, disparos_j1)
        disparos_restantes_j1 -= 1
        print(" Acertaste!" if acierto else " Fallaste.")
        print("Barcos restantes de J2:", contar_barcos_restantes(tablero_j2))
        print("Disparos restantes de J1:", disparos_restantes_j1)
        print("\nTablero de J2 (lo que J1 ve):")
        imprimir_tablero(tablero_j2, oculto=True)
        if all(v == 0 for v in contar_barcos_restantes(tablero_j2).values()):
            print("🎉 J1 ganó!")
            break

        # Turno J2
        print("\nTurno de J2")
        x, y = pedir_coordenada(jugador2, disparos_j2)
        acierto = procesar_disparo(x, y, tablero_j1, disparos_j2)
        disparos_restantes_j2 -= 1
        print(" Acertaste!" if acierto else " Fallaste.")
        print("Barcos restantes de J1:", contar_barcos_restantes(tablero_j1))
        print("Disparos restantes de J2:", disparos_restantes_j2)
        print("\nTablero de J1 (lo que J2 ve):")
        imprimir_tablero(tablero_j1, oculto=True)
        if all(v == 0 for v in contar_barcos_restantes(tablero_j1).values()):
            print("🎉 J2 ganó!")
            break

        turno += 1

    print("\n=== FIN DEL JUEGO ===")


def jugar_j1_vs_maquina():
    print("\n=== MODO: J1 vs MÁQUINA ===")
    tablero_j1 = colocar_todos_los_barcos(obtener_matriz_inicial())
    tablero_m = colocar_todos_los_barcos(obtener_matriz_inicial())
    disparos_j1, disparos_m = set(), set()
    disparos_restantes_j1, disparos_restantes_m = disparos_totales, disparos_totales
    turno = 1

    # Mostrar tablero inicial del jugador (oculto)
    print("\nTablero de J1 (oculto para la máquina):")
    imprimir_tablero(tablero_j1, oculto=True)

    while disparos_restantes_j1 > 0 and disparos_restantes_m > 0:
        print(f"\n===== RONDA {turno} =====")
        
        # Turno J1
        print("\nTurno de J1")
        x, y = pedir_coordenada(jugador1, disparos_j1)
        acierto = procesar_disparo(x, y, tablero_m, disparos_j1)
        disparos_restantes_j1 -= 1
        print(" Acertaste!" if acierto else " Fallaste.")
        print("Barcos restantes de Máquina:", contar_barcos_restantes(tablero_m))
        print("Disparos restantes de J1:", disparos_restantes_j1)
        print("\nTablero de la Máquina (lo que J1 ve):")
        imprimir_tablero(tablero_m, oculto=True)
        if all(v == 0 for v in contar_barcos_restantes(tablero_m).values()):
            print("🎉 J1 ganó!")
            break

        # Turno Máquina
        print("\nTurno de la Máquina")
        x, y = pedir_coordenada(maquina, disparos_m)
        acierto = procesar_disparo(x, y, tablero_j1, disparos_m)
        disparos_restantes_m -= 1
        print("🤖 La máquina acertó!" if acierto else "🤖 La máquina falló.")
        print("Barcos restantes de J1:", contar_barcos_restantes(tablero_j1))
        print("Disparos restantes de Máquina:", disparos_restantes_m)
        print("\nTablero de J1 (lo que J1 ve, oculto para la máquina):")
        imprimir_tablero(tablero_j1, oculto=True)
        if all(v == 0 for v in contar_barcos_restantes(tablero_j1).values()):
            print("💀 La máquina ganó!")
            break

        turno += 1

    print("\n=== FIN DEL JUEGO ===")

    
# Modo debug: función para mostrar todo el tablero (barcos y disparos)
# def imprimir_tablero_completo(matriz): 
#     """Muestra TODO el tablero (barcos, disparos y mar) — solo para pruebas/debug."""
#     imprimir_separador_vertical()
#     separador_numeros()
#     imprimir_separador_vertical()

#     for y in range(filas):
#         print(f"|  {chr(ord('A') + y)}  ", end="")  # Etiqueta de fila (A, B, C...)
#         for x in range(columnas):
#             celda = matriz[y][x]
#             # Si está vacío (mar), mostramos '.' para verlo; si no, mostramos el contenido (barco o disparo)
#             if celda == mar or celda == " ":
#                 mostrar = "."
#             else:
#                 mostrar = celda
#             print(f"|  {mostrar}  ", end="")
#         print("|")
#         imprimir_separador_vertical()


# Modo debug: mostrar tablero completo (con barcos)
# print("\n[DEBUG] Tablero completo (barcos visibles):")
# imprimir_tablero_completo(tablero)

print("===== BIENVENIDO A BATALLA NAVAL =====")

while True:
    print("\n===== MENÚ PRINCIPAL =====")
    print("1. Jugar")
    print("2. Instrucciones")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        print("\n--- Selección de modo de juego ---")
        print("1. Jugador 1 vs Jugador 2")
        print("2. Jugador 1 vs Máquina")
        modo = input("Elija una opción: ")

        if modo == "1":
            jugar_j1_vs_j2()
        elif modo == "2":
            jugar_j1_vs_maquina()
        else:
            print(" Opción inválida en el modo de juego.")

    elif opcion == "2":
        print("\n📜 INSTRUCCIONES DEL JUEGO 📜")
        print("1. Cada jugador tiene un tablero oculto con barcos.")
        print("2. Los barcos se colocan automáticamente de forma aleatoria.")
        print("3. En cada turno el jugador elige una coordenada para disparar.")
        print("4. Si acierta, se marca con 'O'; si falla, con 'X'.")
        print("5. Gana el jugador que hunda todos los barcos del rival.")
        print("6. Cada jugador tiene un número limitado de disparos.")

    elif opcion == "3":
        print("\n👋 Gracias por jugar. ¡Hasta la próxima!")
        break

    else:
        print(" Opción inválida, intente de nuevo.")


# ===================== EDITS =====================
#Se tiene un error en el juego a la hora de el numero de barcos hay mas de los que deberia haber
#se tiene que agregar un contar de los barcos maximos con los que se incia y ver si se estan colocando bien
#y si se estan quitando bien a la hora de que un jugador le acierte a otro

