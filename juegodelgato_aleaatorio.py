#JUEGO DEL GATO

import pygame
import sys
import numpy as np
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 6
BOARD_ROWS, BOARD_COLS = 3, 3
BOARD_SIZE = WIDTH // 3
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)

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
            if board[row][col] == 1:
                pygame.draw.circle(screen, LINE_COLOR, (col * BOARD_SIZE + BOARD_SIZE // 2, row * BOARD_SIZE + BOARD_SIZE // 2), BOARD_SIZE // 3, LINE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, LINE_COLOR, (col * BOARD_SIZE + BOARD_SIZE // 4, row * BOARD_SIZE + BOARD_SIZE // 4), 
                                 (col * BOARD_SIZE + 3 * BOARD_SIZE // 4, row * BOARD_SIZE + 3 * BOARD_SIZE // 4), LINE_WIDTH)
                pygame.draw.line(screen, LINE_COLOR, (col * BOARD_SIZE + BOARD_SIZE // 4, row * BOARD_SIZE + 3 * BOARD_SIZE // 4), 
                                 (col * BOARD_SIZE + 3 * BOARD_SIZE // 4, row * BOARD_SIZE + BOARD_SIZE // 4), LINE_WIDTH)

# Función para realizar una jugada del jugador humano
def make_move(row, col, player):
    if board[row][col] == 0:
        board[row][col] = player

# Función para que la computadora realice una jugada aleatoria
def computer_move():
    empty_cells = np.argwhere(board == 0)
    if len(empty_cells) > 0:
        cell = random.choice(empty_cells)
        board[cell[0]][cell[1]] = 2

# Función para verificar si hay un ganador
def check_winner(player):
    # Verificar filas y columnas
    for i in range(BOARD_ROWS):
        if all(board[i] == player) or all(board[:, i] == player):
            return True
    # Verificar diagonales
    if all(np.diag(board) == player) or all(np.diag(np.fliplr(board)) == player):
        return True
    return False

# Bucle principal del juego
running = True
player = 1

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
                running = False
            player = 2
        if player == 2:
            computer_move()
            if check_winner(2):
                print("¡La computadora ha ganado!")
                running = False
            player = 1

    draw_board()
    draw_symbols()
    pygame.display.update()