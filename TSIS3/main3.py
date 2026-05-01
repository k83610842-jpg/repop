# main.py is the entry point of the game
import pygame, sys
from pygame.locals import *
from persistence import load_settings, save_settings, load_leaderboard, save_leaderboard
from ui import show_main_menu, show_settings, show_leaderboard_screen, show_game_over, get_username
from racer import run_game

# here we initialize pygame
pygame.init()

FPS = 60
clock = pygame.time.Clock()
surface = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Racer Game")

# here we load settings at startup
settings = load_settings()

# here we run the main menu loop
while True:
    choice = show_main_menu(surface, clock)

    if choice == "leaderboard":
        show_leaderboard_screen(surface, clock)

    elif choice == "settings":
        show_settings(surface, clock, settings, save_settings)

    elif choice == "play":
        username = get_username(surface, clock)
        while True:
            # here we run the game and get results when player dies
            final_score, final_dist, final_coins = run_game(surface, clock, username, settings)

            # here we save result to leaderboard
            leaderboard = load_leaderboard()
            leaderboard.append({"name": username, "score": final_score, "distance": final_dist})
            save_leaderboard(leaderboard)

            # here we show game over screen and check what player wants
            result = show_game_over(surface, clock, final_score, final_dist, final_coins)
            if result == "menu":
                break