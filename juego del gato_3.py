import pygame
import sys
import numpy as np
import random
#%%
# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 800
LINE_WIDTH = 6
BOARD_ROWS, BOARD_COLS = 3, 3
BOARD_SIZE = WIDTH // 3
BG_COLOR = (255, 255, 255)
LINE_COLOR = (255, 150, 100)

# Crear la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego del Gato")

# Tablero del juego
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Función para dibujar el tablero
def draw_board():
    screen.fill(BG_COLOR)
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * BOARD_SIZE), (WIDTH, i * BOARD_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * BOARD_SIZE, 0), (i * BOARD_SIZE, HEIGHT), LINE_WIDTH)

# Función para dibujar las fichas
def draw_symbols():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:#COMPRUEBA Si la casilla esta ocupada por otro jugador
                pygame.draw.circle(screen, LINE_COLOR, (col * BOARD_SIZE + BOARD_SIZE // 2, row * BOARD_SIZE + BOARD_SIZE // 2), BOARD_SIZE // 3, LINE_WIDTH) #dibuja un circulo
            elif board[row][col] == 2:
                pygame.draw.line(screen, LINE_COLOR, (col * BOARD_SIZE + BOARD_SIZE // 4, row * BOARD_SIZE + BOARD_SIZE // 4), 
                                 (col * BOARD_SIZE + 3 * BOARD_SIZE // 4, row * BOARD_SIZE + 3 * BOARD_SIZE // 4), LINE_WIDTH)
                pygame.draw.line(screen, LINE_COLOR, (col * BOARD_SIZE + BOARD_SIZE // 4, row * BOARD_SIZE + 3 * BOARD_SIZE // 4), 
                                 (col * BOARD_SIZE + 3 * BOARD_SIZE // 4, row * BOARD_SIZE + BOARD_SIZE // 4), LINE_WIDTH)    #dibuja una x
#%%
# Secuencias ganadoras
winning_sequences = [
    [1, 2, 3],
    [1, 5, 9],
    [1, 4, 7],
    [2, 5, 8],
    [3, 5, 7],
    [3, 6, 9],
    [4, 5, 6],
    [7, 8, 9]]

# Función para realizar una jugada del jugador humano
def make_move(row, col, player):
    if board[row][col] == 0: #verifica si la casilla esta vacia
        board[row][col] = player #asigna el numero de casilla

# Función para verificar si hay un ganador
def check_winner(player):
    for seq in winning_sequences: #itera sobre cada secuencia ganadora
        if all(board[(num - 1) // BOARD_ROWS][(num - 1) % BOARD_COLS] == player for num in seq): #Comprueba si todas las casillas en una secuencia ganadora están ocupadas por el jugador especificado
            return True
    return False

# Función para verificar si hay un empate
def check_draw():
    return np.all(board != 0) and not any(check_winner(1) for seq in winning_sequences) and not any(check_winner(2) for seq in winning_sequences)

# Función para bloquear al jugador si está a punto de ganar
def block_player(player):
    for seq in winning_sequences:#itera sobre cada secuencia ganadora
        count_player = 0 #casillas ocupadas
        count_empty = 0 #casillas vacias
        for num in seq:
            row = (num - 1) // BOARD_ROWS
            col = (num - 1) % BOARD_COLS #calcula las coordenadas de fila y columna
            if board[row][col] == player:
                count_player += 1
            elif board[row][col] == 0:
                count_empty += 1
        if count_player == 2 and count_empty == 1: #Comprueba si el jugador tiene dos casillas ocupadas y una vacía en la secuencia
            for num in seq:
                row = (num - 1) // BOARD_ROWS
                col = (num - 1) % BOARD_COLS
                if board[row][col] == 0: #detecta la casilla vacia
                    return row, col #devuelve coordenadas de la casilla vacia
    return None

# Función para que la computadora realice una jugada
def computer_move():
    
    # Si es el primer turno, realizar una jugada aleatoria
    if np.sum(board) == 0:
        row = random.randint(0, BOARD_ROWS - 1)
        col = random.randint(0, BOARD_COLS - 1)
        make_move(row, col, 2)
        player = 1
        return
    
    
    # Bloquear al jugador si está a punto de ganar
    move = block_player(1)
    if move:
        make_move(move[0], move[1], 2)# comprueba si hay bloqueo
        return

    # Realizar una jugada siguiendo las secuencias ganadoras
    for seq in winning_sequences:
        count_player = 0
        count_empty = 0
        for num in seq:
            row = (num - 1) // BOARD_ROWS
            col = (num - 1) % BOARD_COLS
            if board[row][col] == 2:
                count_player += 1
            elif board[row][col] == 0:
                count_empty += 1
        if count_player == 2 and count_empty == 1:
            for num in seq:
                row = (num - 1) // BOARD_ROWS
                col = (num - 1) % BOARD_COLS
                if board[row][col] == 0:#detecta si la casilla esta vacia
                    make_move(row, col, 2)# juega la computadora
                    return
#%%

    # Calcular la probabilidad de ganar para cada casilla vacía
    empty_cells = np.argwhere(board == 0) #Se obtienen las coordenadas de todas las casillas vacías en el tablero.
    best_move = None #mejor casilla
    best_prob = -10 #probabilidad de ganar inicial
    
    for cell in empty_cells:
        row, col = cell
        prob = random.random()
        if prob > best_prob:
            best_prob = prob
            best_move = (row, col)
    
    # Realizar el mejor movimiento en función de las probabilidades
    if best_move:
        make_move(best_move[0], best_move[1], 2)


#%%
# Función para reiniciar el juego
def reset_game():
    global board
    board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Bucle principal del juego
running = True
player = random.choice([1, 2])  # Determinar aleatoriamente quién empieza

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and player == 1:
            x, y = event.pos
            row = y // BOARD_SIZE
            col = x // BOARD_SIZE
            make_move(row, col, player)
            if check_winner(player):
                print("¡Has ganado!")
                reset_game()
            elif check_draw():
                print("¡Empate!")
                reset_game()
            player = 2
        if player == 2:
            computer_move()
            if check_winner(2):
                print("¡La computadora ha ganado!")
                reset_game()
            elif check_draw():
                print("¡Empate!")
                reset_game()
            player = 1

    draw_board()
    draw_symbols()
    pygame.display.update()
