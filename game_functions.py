import numpy as np
import pygame
import math
import random

def create_board(c4_settings):
    board = np.zeros((c4_settings.row_count, c4_settings.column_count))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[5][col] == 0

def get_next_open_row(c4_settings, board, col):
    for row in range(c4_settings.row_count):
        if board[row][col] == 0:
            return row

def print_board(board):
    print(np.flip(board, 0))

def draw_board(c4_settings, board, screen):
    for col in range(c4_settings.column_count):
        for row in range(c4_settings.row_count):
            pygame.draw.rect(screen, c4_settings.blue, (col*c4_settings.square, row*c4_settings.square+c4_settings.square, c4_settings.square, c4_settings.square))
            pygame.draw.circle(screen, c4_settings.black, (int(col*c4_settings.square+c4_settings.square/2), int(row*c4_settings.square+c4_settings.square+c4_settings.square/2)), c4_settings.radius)

    for col in range(c4_settings.column_count):
        for row in range(c4_settings.row_count):
            if board[row][col] == 1:
                pygame.draw.circle(screen, c4_settings.red, (int(col*c4_settings.square+c4_settings.square/2), c4_settings.height-int(row*c4_settings.square+c4_settings.square/2)), c4_settings.radius)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, c4_settings.yellow, (int(col*c4_settings.square+c4_settings.square/2), c4_settings.height-int(row*c4_settings.square+c4_settings.square/2)), c4_settings.radius)
    pygame.display.update()

def win_game(c4_settings, board, piece):
    """Determine win cases for game."""

    # Check for horizontal win
    for col in range(c4_settings.column_count-3):
        for row in range(c4_settings.row_count):
            count = 0
            while board[row][col+count] == piece:
                if count >= 3:
                    return True
                count+=1

    #Check for vertical win
    for col in range(c4_settings.column_count):
        for row in range(c4_settings.row_count-3):
            count = 0
            while board[row+count][col] == piece:
                if count >= 3:
                    return True
                count+=1

    # Check for diagonal up
    for col in range(c4_settings.column_count-3):
        for row in range(c4_settings.row_count-3):
            count = 0
            while board[row+count][col+count] == piece:
                if count >= 3:
                    return True
                count+=1

    # Check for diagonal down
    for col in range(c4_settings.column_count-3):
        for row in range(c4_settings.row_count):
            count = 0
            while board[row-count][col+count] == piece:
                if count >= 3:
                    return True
                count+=1

def reset_board(c4_settings, board, row, col):
    for col in range(c4_settings.column_count):
        for row in range(c4_settings.row_count):
            board[row][col] = 0

def evaluate_window(c4_settings, window, piece):
    score = 0
    opponent_piece = c4_settings.player_piece
    if piece == c4_settings.player_piece:
        opponent_piece = c4_settings.ai_piece
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(c4_settings.empty) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(c4_settings.empty) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(c4_settings.empty) == 1:
        score -= 4

    return score

def score_position(c4_settings, board, piece):
    score = 0

    ## Score centre
    center_array = [int(i) for i in list(board[:, c4_settings.column_count//2])]
    center_count = center_array.count(piece)
    score += center_count * 3


    ## Score Horizontal
    for row in range(c4_settings.row_count):
        row_array = [int(index) for index in list(board[row,:])]
        for col in range(c4_settings.column_count-3):
            window = row_array[col:col+c4_settings.window_length]
            score += evaluate_window(c4_settings, window, piece)

    ## Score Vertical
    for col in range(c4_settings.column_count):
        col_array = [int(i) for i in list(board[:,col])]
        for row in range(c4_settings.row_count-3):  
            window = col_array[row:row+c4_settings.window_length]
            score += evaluate_window(c4_settings, window, piece)        

    ## Score positive diagonals
    for row in range(c4_settings.row_count-3):
        for col in range(c4_settings.column_count-3):
            window = [board[row+i][col+i] for i in range(c4_settings.window_length)]
            score += evaluate_window(c4_settings, window, piece)

    ## Score negative diagonals
    for row in range(c4_settings.row_count-3):
        for col in range(c4_settings.column_count-3):
            window = [board[row+3-i][col+i] for i in range(c4_settings.window_length)]
            score += evaluate_window(c4_settings, window, piece)
    return score

def terminal_node(c4_settings, board):
    return win_game(c4_settings, board, c4_settings.player_piece) or win_game(c4_settings, board, c4_settings.ai_piece) or len(get_valid_locations(c4_settings, board)) == 0

def minimax(c4_settings, board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(c4_settings, board)
    terminal = terminal_node(c4_settings, board)
    if depth == 0 or terminal:
        if terminal:
            if win_game(c4_settings, board, c4_settings.ai_piece):
                return (None, 100000000000)
            elif win_game(c4_settings, board, c4_settings.player_piece):
                return (None, -10000000000)
            else: # Game is over, board is full
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(c4_settings, board, c4_settings.ai_piece))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(c4_settings, board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, c4_settings.ai_piece)
            new_score = minimax(c4_settings, board_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: #Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(c4_settings, board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, c4_settings.player_piece)
            new_score = minimax(c4_settings, board_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(c4_settings, board):
    valid_locations = []
    for col in range(c4_settings.column_count):
        if is_valid_location(board, col):
            valid_locations.append(col)

    return valid_locations

def pick_best_move(c4_settings, board, piece):
    best_score = 0
    valid_locations = get_valid_locations(c4_settings, board)
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(c4_settings, board, col)
        simulate_board = board.copy()
        drop_piece(simulate_board, row, col, piece)
        score = score_position(c4_settings, simulate_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col



