# ui.py handles all screens and buttons
import pygame, sys
from pygame.locals import *
from persistence import load_leaderboard

FPS = 60
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

# here we draw a simple button and return its rect
def draw_button(surface, text, x, y, w, h, color):
    font_small = pygame.font.SysFont("Verdana", 20)
    pygame.draw.rect(surface, color, (x, y, w, h))
    label = font_small.render(text, True, WHITE)
    surface.blit(label, (x + 10, y + 10))
    return pygame.Rect(x, y, w, h)

# here we show the main menu screen
def show_main_menu(surface, clock):
    font_mid = pygame.font.SysFont("Verdana", 30)
    while True:
        surface.fill(BLACK)
        title = font_mid.render("RACER GAME", True, (255, 255, 0))
        surface.blit(title, (100, 80))
        btn_play = draw_button(surface, "Play",        120, 180, 160, 45, (0, 150, 0))
        btn_lb   = draw_button(surface, "Leaderboard", 120, 245, 160, 45, (0, 100, 200))
        btn_set  = draw_button(surface, "Settings",    120, 310, 160, 45, (150, 100, 0))
        btn_quit = draw_button(surface, "Quit",        120, 375, 160, 45, (180, 0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if btn_play.collidepoint(event.pos):
                    return "play"
                if btn_lb.collidepoint(event.pos):
                    return "leaderboard"
                if btn_set.collidepoint(event.pos):
                    return "settings"
                if btn_quit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        clock.tick(FPS)

# here we show the settings screen
def show_settings(surface, clock, settings, save_settings):
    font_mid = pygame.font.SysFont("Verdana", 30)
    while True:
        surface.fill(BLACK)
        title = font_mid.render("SETTINGS", True, (255, 255, 0))
        surface.blit(title, (130, 40))
        sound_label = "Sound: ON" if settings["sound"] else "Sound: OFF"
        btn_sound = draw_button(surface, sound_label,                             80, 130, 240, 45, (0, 120, 120))
        btn_color = draw_button(surface, "Car: " + settings["car_color"],         80, 195, 240, 45, (120, 0, 120))
        btn_diff  = draw_button(surface, "Difficulty: " + settings["difficulty"], 80, 260, 240, 45, (120, 80, 0))
        btn_back  = draw_button(surface, "Back",                                  80, 360, 240, 45, (180, 0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if btn_sound.collidepoint(event.pos):
                    # here we toggle sound on or off
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)
                if btn_color.collidepoint(event.pos):
                    # here we cycle through car colors
                    colors = ["red", "blue", "green", "yellow"]
                    i = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(i + 1) % len(colors)]
                    save_settings(settings)
                if btn_diff.collidepoint(event.pos):
                    # here we cycle through difficulty levels
                    diffs = ["easy", "normal", "hard"]
                    i = diffs.index(settings["difficulty"])
                    settings["difficulty"] = diffs[(i + 1) % len(diffs)]
                    save_settings(settings)
                if btn_back.collidepoint(event.pos):
                    return
        clock.tick(FPS)

# here we show leaderboard screen with top 10
def show_leaderboard_screen(surface, clock):
    font_small = pygame.font.SysFont("Verdana", 20)
    font_mid   = pygame.font.SysFont("Verdana", 30)
    leaderboard = load_leaderboard()
    while True:
        surface.fill(BLACK)
        title = font_mid.render("TOP 10 SCORES", True, (255, 255, 0))
        surface.blit(title, (70, 20))
        sorted_lb = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
        for i, entry in enumerate(sorted_lb):
            line = str(i+1) + ". " + entry["name"] + "  " + str(entry["score"]) + "  " + str(entry["distance"]) + "m"
            line_text = font_small.render(line, True, WHITE)
            surface.blit(line_text, (20, 70 + i * 42))
        btn_back = draw_button(surface, "Back", 130, 540, 140, 40, (180, 0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if btn_back.collidepoint(event.pos):
                    return
        clock.tick(FPS)

# here we show game over screen with final stats
def show_game_over(surface, clock, total_score, distance, coin_count):
    font      = pygame.font.SysFont("Verdana", 60)
    font_small = pygame.font.SysFont("Verdana", 20)
    while True:
        surface.fill(RED)
        go_text    = font.render("Game Over", True, BLACK)
        score_text = font_small.render("Score:    " + str(total_score), True, WHITE)
        dist_text  = font_small.render("Distance: " + str(distance) + "m", True, WHITE)
        coins_text = font_small.render("Coins:    " + str(coin_count), True, WHITE)
        surface.blit(go_text,    (30, 80))
        surface.blit(score_text, (120, 200))
        surface.blit(dist_text,  (120, 230))
        surface.blit(coins_text, (120, 260))
        btn_retry = draw_button(surface, "Retry",     80, 340, 140, 45, (0, 150, 0))
        btn_menu  = draw_button(surface, "Main Menu", 80, 400, 140, 45, (0, 100, 200))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if btn_retry.collidepoint(event.pos):
                    return "retry"
                if btn_menu.collidepoint(event.pos):
                    return "menu"
        clock.tick(FPS)

# here we ask player to type their name
def get_username(surface, clock):
    font_small = pygame.font.SysFont("Verdana", 20)
    font_mid   = pygame.font.SysFont("Verdana", 30)
    name = ""
    while True:
        surface.fill(BLACK)
        prompt    = font_small.render("Enter your name:", True, WHITE)
        name_text = font_mid.render(name, True, (255, 255, 0))
        hint      = font_small.render("Press ENTER to start", True, (150, 150, 150))
        surface.blit(prompt,    (80, 220))
        surface.blit(name_text, (80, 270))
        surface.blit(hint,      (80, 320))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN and name != "":
                    return name
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12:
                        name += event.unicode
        clock.tick(FPS)
