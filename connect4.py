import pygame
from settings import Settings
import game_functions as gf
from button import Button
from time import sleep
import sys
import math
import random

def run_game():
    c4_settings = Settings()
    board = gf.create_board(c4_settings)
    game_active = False
    turn = 0

    pygame.init()
    myfont = pygame.font.SysFont("ariel", 80)
    screen = pygame.display.set_mode((c4_settings.width, c4_settings.height))
    screen.fill(c4_settings.black)
    pygame.display.set_caption("Connect Four")
    gf.draw_board(c4_settings, board, screen)
    play_button = Button(c4_settings, screen, "Press Enter to Start")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_active = True
                    gf.draw_board(c4_settings, board, screen)

            if not game_active:
                play_button.draw_button()
                pygame.display.flip()             

            if game_active:
                if event.type == pygame.MOUSEMOTION:
                    pygame.display.flip()
                    pygame.draw.rect(screen, c4_settings.black, (0, 0, c4_settings.width, c4_settings.square))
                    posx = event.pos[0]
                    pygame.draw.circle(screen, c4_settings.red, (posx, int(c4_settings.square/2)), c4_settings.radius)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Ask for Player 1 Input
                    if turn == c4_settings.player:
                        posx = event.pos[0]
                        col = int(math.floor(posx/c4_settings.square))

                        if gf.is_valid_location(board, col):
                            row = gf.get_next_open_row(c4_settings, board, col)
                            gf.drop_piece(board, row, col, 1)
                            gf.draw_board(c4_settings, board, screen)

                            if gf.win_game(c4_settings, board, 1):
                                print("Player 1 wins!")
                                label = myfont.render("Player 1 Wins!", 1, c4_settings.white)
                                screen.blit(label, (40, 10))
                                game_active = False
                                gf.reset_board(c4_settings, board, row, col)  

                            turn += 1
                            turn = turn % 2
                    pygame.display.update()

            if turn == c4_settings.ai and game_active:
                col, minimax_score = gf.minimax(c4_settings, board, 5, -math.inf, math.inf, True)

                if gf.is_valid_location(board, col):
                    row = gf.get_next_open_row(c4_settings, board, col)
                    gf.drop_piece(board, row, col, 2)
                    gf.draw_board(c4_settings, board, screen)

                    if gf.win_game(c4_settings, board, 2):
                        print("AI wins!")
                        label = myfont.render("AI Wins!", 2, c4_settings.white)
                        screen.blit(label, (40, 10))                                
                        game_active = False
                        gf.reset_board(c4_settings, board, row, col)  

                    turn += 1
                    turn = turn % 2

            pygame.display.flip()
run_game()