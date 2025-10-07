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

# Cantidades de barcos (por tipo)
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
    return chr(ord(letra) + 1)

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

def colocar_barco(matriz, longitud, tipo_barco, cantidad, ships=None):
    """
    Coloca 'cantidad' barcos de 'longitud' y 'tipo_barco' en 'matriz'.
    Si se pasa 'ships' (lista), agrega una entrada por cada barco con sus coordenadas.
    """
    barcos_colocados = 0
    intentos_max = 1000
    intentos = 0

    while barcos_colocados < cantidad and intentos < intentos_max:
        intentos += 1
        x = obtener_x_aleatorio()
        y = obtener_y_aleatorio()
        orientacion = random.choice(["H", "V"])

        if orientacion == "H" and x + longitud - 1 < columnas:
            if all(coordenada_vacia(x+i, y, matriz) for i in range(longitud)):
                coords = []
                for i in range(longitud):
                    matriz[y][x+i] = tipo_barco
                    coords.append((x+i, y))
                barcos_colocados += 1
                if ships is not None:
                    ships.append({"tipo": tipo_barco, "coords": coords, "sunk": False})

        elif orientacion == "V" and y + longitud - 1 < filas:
            if all(coordenada_vacia(x, y+i, matriz) for i in range(longitud)):
                coords = []
                for i in range(longitud):
                    matriz[y+i][x] = tipo_barco
                    coords.append((x, y+i))
                barcos_colocados += 1
                if ships is not None:
                    ships.append({"tipo": tipo_barco, "coords": coords, "sunk": False})

    return matriz

def colocar_todos_los_barcos(matriz, ships=None):
    """
    Coloca todos los barcos en 'matriz'. Si se pasa 'ships' (lista), se llenará con
    la información de cada barco colocado.
    """
    matriz = colocar_barco(matriz, 1, submarino, cantidad_submarinos, ships)
    matriz = colocar_barco(matriz, 2, crucero, cantidad_cruceros, ships)
    matriz = colocar_barco(matriz, 3, destructor, cantidad_destructores, ships)
    matriz = colocar_barco(matriz, 4, acorazado, cantidad_acorazados, ships)
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
            if not numero.isdigit():
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

def procesar_disparo(x, y, tablero, disparos_realizados, ships=None):
    """
    Procesa el disparo en (x,y) sobre 'tablero'.
    Si 'ships' se proporciona (lista de barcos del tablero), actualiza su estado y
    detecta si un barco quedó totalmente hundido.
    Devuelve True si fue acierto, False si fallo.
    """
    disparos_realizados.add((x, y))
    if tablero[y][x] in [submarino, crucero, destructor, acorazado]:
        tablero[y][x] = disparo_acertado
        try:
            sonido_disparo_acertado.play()
        except Exception:
            pass

        # Si tenemos la lista de barcos, actualizar su estado y detectar hundimiento
        if ships is not None:
            # Mapeo para mensajes
            nombre_sing = {submarino: "submarino", crucero: "crucero", destructor: "destructor", acorazado: "acorazado"}
            for ship in ships:
                if (x, y) in ship["coords"] and not ship["sunk"]:
                    # Comprueba si todas sus coordenadas están marcadas como disparo_acertado en el tablero
                    if all(tablero[cy][cx] == disparo_acertado for (cx, cy) in ship["coords"]):
                        ship["sunk"] = True
                        print(f"¡Hundiste un {nombre_sing[ship['tipo']]}!")  # Mensaje de hundimiento
                    break

        return True
    else:
        tablero[y][x] = disparo_fallado
        try:
            sonido_disparo_fallado.play()
        except Exception:
            pass
        return False

def contar_barcos_restantes_por_ships(ships):
    """
    Recibe la lista de barcos (cada uno con 'tipo' y 'sunk') y devuelve un dict
    con la cantidad de barcos no hundidos por tipo.
    """
    conteo = {"Submarinos": 0, "Cruceros": 0, "Destructores": 0, "Acorazados": 0}
    for ship in ships:
        if not ship.get("sunk", False):
            if ship["tipo"] == submarino:
                conteo["Submarinos"] += 1
            elif ship["tipo"] == crucero:
                conteo["Cruceros"] += 1
            elif ship["tipo"] == destructor:
                conteo["Destructores"] += 1
            elif ship["tipo"] == acorazado:
                conteo["Acorazados"] += 1
    return conteo

def reconstruir_ships(matriz):
    """
    Reconstruye la lista 'ships' examinando el tablero y agrupando celdas contiguas
    del mismo tipo de barco (horizontal/vertical).
    """
    ships = []
    visited = [[False]*columnas for _ in range(filas)]
    for y in range(filas):
        for x in range(columnas):
            celda = matriz[y][x]
            if celda in [submarino, crucero, destructor, acorazado] and not visited[y][x]:
                tipo = celda
                stack = [(x,y)]
                coords = []
                visited[y][x] = True
                while stack:
                    cx, cy = stack.pop()
                    coords.append((cx, cy))
                    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < columnas and 0 <= ny < filas and not visited[ny][nx] and matriz[ny][nx] == tipo:
                            visited[ny][nx] = True
                            stack.append((nx, ny))
                ships.append({"tipo": tipo, "coords": coords, "sunk": False})
    return ships

# ===================== FUNCIONES DE PARTIDA =====================

def jugar_j1_vs_j2(tablero_j1=None, tablero_j2=None, ships_j1=None, ships_j2=None):
    """
    Juega J1 vs J2. Si se pasan tableros y ships, se usan; si no, los genera/reconstruye.
    """
    print("\n=== MODO: J1 vs J2 ===")

    # Preparar tableros y ships (usar los recibidos si existen)
    if tablero_j1 is None:
        ships_j1 = [] if ships_j1 is None else ships_j1
        tablero_j1 = colocar_todos_los_barcos(obtener_matriz_inicial(), ships_j1)
    else:
        if ships_j1 is None:
            ships_j1 = reconstruir_ships(tablero_j1)

    if tablero_j2 is None:
        ships_j2 = [] if ships_j2 is None else ships_j2
        tablero_j2 = colocar_todos_los_barcos(obtener_matriz_inicial(), ships_j2)
    else:
        if ships_j2 is None:
            ships_j2 = reconstruir_ships(tablero_j2)

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
        acierto = procesar_disparo(x, y, tablero_j2, disparos_j1, ships_j2)
        disparos_restantes_j1 -= 1
        print(" Acertaste!" if acierto else " Fallaste.")
        print("Barcos restantes de J2:", contar_barcos_restantes_por_ships(ships_j2))
        print("Disparos restantes de J1:", disparos_restantes_j1)
        print("\nTablero de J2 (lo que J1 ve):")
        imprimir_tablero(tablero_j2, oculto=True)
        if all(ship["sunk"] for ship in ships_j2):
            print("J1 ganó!")
            break

        # Turno J2
        print("\nTurno de J2")
        x, y = pedir_coordenada(jugador2, disparos_j2)
        acierto = procesar_disparo(x, y, tablero_j1, disparos_j2, ships_j1)
        disparos_restantes_j2 -= 1
        print(" Acertaste!" if acierto else " Fallaste.")
        print("Barcos restantes de J1:", contar_barcos_restantes_por_ships(ships_j1))
        print("Disparos restantes de J2:", disparos_restantes_j2)
        print("\nTablero de J1 (lo que J2 ve):")
        imprimir_tablero(tablero_j1, oculto=True)
        if all(ship["sunk"] for ship in ships_j1):
            print("J2 ganó!")
            break

        turno += 1

    print("\n=== FIN DEL JUEGO ===")


def jugar_j1_vs_maquina(tablero_j1=None, tablero_m=None, ships_j1=None, ships_m=None):
    """
    Juega J1 vs Máquina. Si se pasan tableros y ships, se usan; si no, los genera/reconstruye.
    """
    print("\n=== MODO: J1 vs MÁQUINA ===")

    # Preparar tableros y ships (usar los recibidos si existen)
    if tablero_j1 is None:
        ships_j1 = [] if ships_j1 is None else ships_j1
        tablero_j1 = colocar_todos_los_barcos(obtener_matriz_inicial(), ships_j1)
    else:
        if ships_j1 is None:
            ships_j1 = reconstruir_ships(tablero_j1)

    if tablero_m is None:
        ships_m = [] if ships_m is None else ships_m
        tablero_m = colocar_todos_los_barcos(obtener_matriz_inicial(), ships_m)
    else:
        if ships_m is None:
            ships_m = reconstruir_ships(tablero_m)

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
        acierto = procesar_disparo(x, y, tablero_m, disparos_j1, ships_m)
        disparos_restantes_j1 -= 1
        print(" Acertaste!" if acierto else " Fallaste.")
        print("Barcos restantes de Máquina:", contar_barcos_restantes_por_ships(ships_m))
        print("Disparos restantes de J1:", disparos_restantes_j1)
        print("\nTablero de la Máquina (lo que J1 ve):")
        imprimir_tablero(tablero_m, oculto=True)
        if all(ship["sunk"] for ship in ships_m):
            print("J1 ganó!")
            break

        # Turno Máquina
        print("\nTurno de la Máquina")
        x, y = pedir_coordenada(maquina, disparos_m)
        acierto = procesar_disparo(x, y, tablero_j1, disparos_m, ships_j1)
        disparos_restantes_m -= 1
        print("La máquina acertó!" if acierto else "La máquina falló.")
        print("Barcos restantes de J1:", contar_barcos_restantes_por_ships(ships_j1))
        print("Disparos restantes de Máquina:", disparos_restantes_m)
        print("\nTablero de J1 (lo que J1 ve, oculto para la máquina):")
        imprimir_tablero(tablero_j1, oculto=True)
        if all(ship["sunk"] for ship in ships_j1):
            print("La máquina ganó!")
            break

        turno += 1

    print("\n=== FIN DEL JUEGO ===")

    
#Modo debug: función para mostrar todo el tablero (barcos y disparos)
def imprimir_tableros_completos(tablero1, tablero2, nombre1="J1", nombre2="J2/Máquina"):
    ancho_tablero = columnas * 7 + 6  # 7 por celda + 6 por separadores verticales
    print(f"{nombre1:^{ancho_tablero}}      {nombre2:^{ancho_tablero}}\n")

    # Separador superior
    for _ in range(columnas + 1):
        print("+-----", end="")
    print("+      ", end="")
    for _ in range(columnas + 1):
        print("+-----", end="")
    print("+")

    # Números de columnas
    print("|     ", end="")
    for x in range(columnas):
        print(f"|  {x+1}  ", end="")
    print("|      ", end="")
    print("|     ", end="")
    for x in range(columnas):
        print(f"|  {x+1}  ", end="")
    print("|")

    # Separador horizontal
    for _ in range(columnas + 1):
        print("+-----", end="")
    print("+      ", end="")
    for _ in range(columnas + 1):
        print("+-----", end="")
    print("+")

    # Filas
    for y in range(filas):
        # Tablero 1
        print(f"|  {chr(ord('A') + y)}  ", end="")
        for x in range(columnas):
            celda = tablero1[y][x]
            mostrar = "." if celda == mar else celda
            print(f"|  {mostrar}  ", end="")
        print("|      ", end="")

        # Tablero 2
        print(f"|  {chr(ord('A') + y)}  ", end="")
        for x in range(columnas):
            celda = tablero2[y][x]
            mostrar = "." if celda == mar else celda
            print(f"|  {mostrar}  ", end="")
        print("|")

        # Separador horizontal de fila
        for _ in range(columnas + 1):
            print("+-----", end="")
        print("+      ", end="")
        for _ in range(columnas + 1):
            print("+-----", end="")
        print("+")


# ===================== BLOQUE PRINCIPAL (DEBUG + MENÚ) =====================

# Generar una vez los tableros de debug y sus ships y mostrarlos.
print("\n[DEBUG] Tablero completo (barcos visibles):")
ships_j1_debug = []
ships_j2_debug = []
tablero_j1 = colocar_todos_los_barcos(obtener_matriz_inicial(), ships_j1_debug)
tablero_j2 = colocar_todos_los_barcos(obtener_matriz_inicial(), ships_j2_debug)
imprimir_tableros_completos(tablero_j1, tablero_j2, "J1", "J2")

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
            # Reutiliza los tableros generados en debug (tablero_j1, tablero_j2) y sus ships
            jugar_j1_vs_j2(tablero_j1=tablero_j1, tablero_j2=tablero_j2, ships_j1=ships_j1_debug, ships_j2=ships_j2_debug)

        elif modo == "2":
            # Para máquina reutilizamos tablero_j2 como tablero de la máquina
            jugar_j1_vs_maquina(tablero_j1=tablero_j1, tablero_m=tablero_j2, ships_j1=ships_j1_debug, ships_m=ships_j2_debug)

        else:
            print(" Opción inválida en el modo de juego.")

    elif opcion == "2":
        print("\n📜 INSTRUCCIONES DEL JUEGO 📜")
        print("1. Cada jugador tiene un tablero oculto con barcos.")
        print("2. Los barcos se colocan automáticamente de forma aleatoria (o usa el debug).")
        print("3. En cada turno el jugador elige una coordenada para disparar.")
        print("4. Si acierta, se marca con 'O'; si falla, con 'X'.")
        print("5. Gana el jugador que hunda todos los barcos del rival.")
        print("6. Cada jugador tiene un número limitado de disparos.")
        print("7. ¡Diviértete y buena suerte!")
        
    elif opcion == "3":
        print("\n👋 Gracias por jugar. ¡Hasta la próxima!")
        break

    else:
        print(" Opción inválida, intente de nuevo.")