# main.py
# точка входа — тут игровой цикл, экраны и кнопки

import pygame
import os

from config import WIDTH, HEIGHT, GRID_TOP, COLS, ROWS, TILE
from game import (
    Snake, Food, PoisonFood, PowerUp, Obstacles,
    ScoreManager, load_settings, save_settings,
)
from db import init_db, get_or_create_player, save_session, get_personal_best, get_top10

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock      = pygame.time.Clock()
font_big   = pygame.font.SysFont("Verdana", 48)
font_med   = pygame.font.SysFont("Verdana", 28)
font_small = pygame.font.SysFont("Verdana", 20)

init_db()
settings = load_settings()  # загружаем настройки сразу при старте (task 3.5)


# --- task 3.6: состояния игры ---
# в какой момент находимся — меню, игра, пауза и тд

class State:
    USERNAME    = "username"
    MENU        = "menu"
    PLAYING     = "playing"
    PAUSED      = "paused"
    GAME_OVER   = "game_over"
    LEADERBOARD = "leaderboard"
    SETTINGS    = "settings"   # новый экран настроек


# --- task 3.6: кнопка ---
# простой класс — знает где находится и рисует себя

class Button:
    def __init__(self, text, cx, cy, w=220, h=44):
        self.text = text
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.center = (cx, cy)  # ставим кнопку по центру

    def draw(self):
        # если мышь над кнопкой — делаю чуть светлее
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        bg  = (80, 80, 180) if hovered else (50, 50, 120)
        brd = (160, 160, 255) if hovered else (100, 100, 200)
        pygame.draw.rect(screen, bg,  self.rect, border_radius=8)
        pygame.draw.rect(screen, brd, self.rect, 2, border_radius=8)
        surf = font_small.render(self.text, True, (255, 255, 255))
        screen.blit(surf, surf.get_rect(center=self.rect.center))

    def clicked(self, event):
        # True если кликнули левой кнопкой мыши именно по этой кнопке
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.rect.collidepoint(event.pos))


# --- вспомогательные функции для рисования ---

def draw_background():
    pygame.draw.rect(screen, (20, 20, 20), (0, 0, WIDTH, GRID_TOP))
    # шахматный фон из двух оттенков серого
    colors = [(30, 30, 30), (40, 40, 40)]
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(screen, colors[(r + c) % 2],
                (c * TILE, GRID_TOP + r * TILE, TILE, TILE))
    # task 3.5: если сетка включена — рисуем линии поверх
    if settings["grid_overlay"]:
        for r in range(ROWS + 1):
            pygame.draw.line(screen, (60, 60, 60),
                (0, GRID_TOP + r * TILE), (WIDTH, GRID_TOP + r * TILE))
        for c in range(COLS + 1):
            pygame.draw.line(screen, (60, 60, 60),
                (c * TILE, GRID_TOP), (c * TILE, HEIGHT))

def draw_hud(score, personal_best, active_effect, effect_end_time, shield_active):
    # верхняя панель с очками, уровнем и рекордом
    screen.blit(font_small.render(f"Очки: {score.current}", True, (255, 255, 255)), (10, 8))
    lv = font_small.render(f"Уровень: {score.level}", True, (100, 200, 255))
    screen.blit(lv, (WIDTH // 2 - lv.get_width() // 2, 8))
    hi = font_small.render(f"Рекорд: {score.high}", True, (255, 215, 0))
    pb = font_small.render(f"Лучший: {personal_best}", True, (180, 255, 180))
    screen.blit(hi, (WIDTH - hi.get_width() - 10, 8))
    screen.blit(pb, (WIDTH - pb.get_width() - 10, 22))
    # показываем активный эффект если есть
    if shield_active:
        screen.blit(font_small.render("SHIELD", True, (255, 230, 0)), (10, 22))
    elif active_effect and pygame.time.get_ticks() < effect_end_time:
        tl  = (effect_end_time - pygame.time.get_ticks()) / 1000
        col = (0, 200, 255) if active_effect == "speed" else (200, 100, 255)
        lbl = "SPEED" if active_effect == "speed" else "SLOW"
        screen.blit(font_small.render(f"{lbl} {tl:.1f}s", True, col), (10, 22))

def draw_center(text, font, y, color=(255, 255, 255)):
    # рисую текст по центру экрана на нужной высоте y
    surf = font.render(text, True, color)
    screen.blit(surf, surf.get_rect(center=(WIDTH // 2, y)))

def draw_overlay():
    # полупрозрачный чёрный фон — чтобы меню читалось поверх игры
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 160))
    screen.blit(s, (0, 0))


# --- task 3.6: создаём все кнопки для всех экранов ---

cx = WIDTH // 2  # центр по горизонтали

# главное меню
b_play   = Button("▶  Играть",       cx, HEIGHT // 2 + 10)
b_leader = Button("🏆  Лидерборд",   cx, HEIGHT // 2 + 65)
b_sett   = Button("⚙  Настройки",    cx, HEIGHT // 2 + 120)
b_quit   = Button("✕  Выйти",        cx, HEIGHT // 2 + 175)

# game over
b_retry  = Button("↺  Заново",       cx, HEIGHT // 2 + 85)
b_tomenu = Button("⌂  Главное меню", cx, HEIGHT // 2 + 140)

# назад из лидерборда
b_back   = Button("← Назад", cx, HEIGHT - 45, w=160, h=38)

# настройки — тогглы и сохранение
b_grid   = Button("", cx, HEIGHT // 2 - 40, w=260, h=44)
b_sound  = Button("", cx, HEIGHT // 2 + 20, w=260, h=44)
b_save   = Button("💾  Сохранить и назад", cx, HEIGHT - 45, w=270, h=44)

# выбор цвета змейки — 5 кнопок в ряд
COLOR_OPTIONS = [
    ("Зелёный",  [0, 220, 0]),
    ("Синий",    [0, 150, 255]),
    ("Жёлтый",  [255, 220, 0]),
    ("Красный",  [220, 50, 50]),
    ("Розовый",  [255, 100, 200]),
]
b_colors = [Button(name, 75 + i * 112, HEIGHT // 2 + 100, w=100, h=36)
            for i, (name, _) in enumerate(COLOR_OPTIONS)]


# --- создаём игровые объекты ---

snake     = Snake()
food      = Food()
obstacles = Obstacles()
food.respawn(snake.body)
score     = ScoreManager()
poison    = PoisonFood()
powerup   = PowerUp()

poison_timer    = 0
powerup_timer   = 0
active_effect   = None   # "speed" / "slow" / None
effect_end_time = 0
shield_active   = False

username      = ""
player_id     = None
personal_best = 0
temp_settings = {}  # копия настроек которую редактируем — сохраняем только по кнопке

state   = State.USERNAME
running = True


def reset_game():
    # сбрасываем всё для новой игры
    global poison_timer, powerup_timer, active_effect, effect_end_time, shield_active
    snake.reset()
    score.reset()
    obstacles.blocks = []
    food.respawn(snake.body)
    poison.active   = False
    powerup.active  = False
    poison_timer    = 0
    powerup_timer   = 0
    active_effect   = None
    effect_end_time = 0
    shield_active   = False


# --- главный цикл ---

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # экран ввода имени
        if state == State.USERNAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip():
                    player_id     = get_or_create_player(username.strip())
                    personal_best = get_personal_best(player_id)
                    state = State.MENU
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 20 and event.unicode.isprintable():
                    username += event.unicode

        # главное меню — обрабатываем клики по кнопкам (task 3.6)
        elif state == State.MENU:
            if b_play.clicked(event):
                reset_game(); state = State.PLAYING
            elif b_leader.clicked(event):
                state = State.LEADERBOARD
            elif b_sett.clicked(event):
                # копируем текущие настройки во временные чтобы можно было отменить
                temp_settings = {k: list(v) if isinstance(v, list) else v
                                 for k, v in settings.items()}
                state = State.SETTINGS
            elif b_quit.clicked(event):
                running = False

        # управление змейкой
        elif state == State.PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = State.PAUSED
                elif event.key == pygame.K_RIGHT and snake.dx != -1:
                    snake.dx, snake.dy = 1, 0
                elif event.key == pygame.K_LEFT and snake.dx != 1:
                    snake.dx, snake.dy = -1, 0
                elif event.key == pygame.K_UP and snake.dy != 1:
                    snake.dx, snake.dy = 0, -1
                elif event.key == pygame.K_DOWN and snake.dy != -1:
                    snake.dx, snake.dy = 0, 1

        elif state == State.PAUSED:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state = State.PLAYING

        # game over — кнопки заново или в меню (task 3.6)
        elif state == State.GAME_OVER:
            if b_retry.clicked(event):
                reset_game(); state = State.PLAYING
            elif b_tomenu.clicked(event):
                state = State.MENU

        # лидерборд — кнопка назад (task 3.6)
        elif state == State.LEADERBOARD:
            if b_back.clicked(event):
                state = State.MENU
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = State.MENU

        # настройки — тогглы и сохранение (task 3.5 + 3.6)
        elif state == State.SETTINGS:
            if b_grid.clicked(event):
                temp_settings["grid_overlay"] = not temp_settings["grid_overlay"]
            elif b_sound.clicked(event):
                temp_settings["sound"] = not temp_settings["sound"]
            elif b_save.clicked(event):
                # применяем и сохраняем в файл
                settings.update(temp_settings)
                save_settings(settings)
                state = State.MENU
            for i, bc in enumerate(b_colors):
                if bc.clicked(event):
                    temp_settings["snake_color"] = list(COLOR_OPTIONS[i][1])
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = State.MENU  # ESC = выйти без сохранения


    # --- логика игры ---

    if state == State.PLAYING:
        snake.move()

        # столкновение со стеной / собой / препятствием (task 3.4)
        if snake.hits_wall() or snake.hits_self() or obstacles.hits(snake.head()):
            if shield_active:
                # щит поглощает один удар и исчезает
                shield_active = False
                snake.body[0][0] -= snake.dx
                snake.body[0][1] -= snake.dy
            else:
                state = State.GAME_OVER
                if player_id:
                    save_session(player_id, score.current, score.level)
                    personal_best = get_personal_best(player_id)

        elif snake.head() == [food.c, food.r]:
            snake.grow = True
            score.add(food.points)
            if score.current // 5 >= score.level:
                score.level += 1
                snake.speed += 2
                # task 3.4: при новом уровне генерим препятствия
                if score.level >= 3:
                    obstacles.generate(score.level, snake.body)
            # еда не спавнится на препятствиях (task 3.4)
            food.respawn(snake.body + obstacles.blocks)

        elif food.is_expired():
            food.respawn(snake.body + obstacles.blocks)

        # логика яда
        poison_timer += 1
        if not poison.active and poison_timer >= snake.speed * 10:
            poison.respawn(snake.body + [[food.c, food.r]] + obstacles.blocks)
            poison_timer = 0
        if poison.is_expired():
            poison.active = False
        if poison.active and snake.head() == [poison.c, poison.r]:
            poison.active = False
            for _ in range(2):
                if len(snake.body) > 1:
                    snake.body.pop()  # яд укорачивает змейку на 2
            if len(snake.body) <= 1:
                state = State.GAME_OVER
                if player_id:
                    save_session(player_id, score.current, score.level)
                    personal_best = get_personal_best(player_id)

        # логика пауэрапов
        if active_effect and pygame.time.get_ticks() >= effect_end_time:
            snake.speed   = 8 + (score.level - 1) * 2  # сбрасываем скорость обратно
            active_effect = None
        powerup_timer += 1
        if not powerup.active and powerup_timer >= snake.speed * 15:
            blocked = snake.body + [[food.c, food.r]] + obstacles.blocks
            if poison.active:
                blocked.append([poison.c, poison.r])
            powerup.respawn(blocked)
            powerup_timer = 0
        if powerup.is_expired():
            powerup.active = False
        if powerup.active and snake.head() == [powerup.c, powerup.r]:
            kind = powerup.kind
            powerup.active = False
            if kind == "speed":
                active_effect   = "speed"
                effect_end_time = pygame.time.get_ticks() + 5000
                snake.speed    += 6
            elif kind == "slow":
                active_effect   = "slow"
                effect_end_time = pygame.time.get_ticks() + 5000
                snake.speed     = max(2, snake.speed - 4)
            elif kind == "shield":
                shield_active = True


    # --- рисуем всё ---

    draw_background()
    obstacles.draw(screen)        # task 3.4
    food.draw(screen, font_small)
    poison.draw(screen, font_small)
    powerup.draw(screen, font_small)
    snake.draw(screen, font_small, settings)  # цвет из настроек (task 3.5)
    draw_hud(score, personal_best, active_effect, effect_end_time, shield_active)

    # --- рисуем нужный экран поверх ---

    if state == State.USERNAME:
        draw_overlay()
        draw_center("ВВЕДИ ИМЯ:", font_small, HEIGHT // 2 - 40)
        ns = font_big.render(username + "|", True, (255, 255, 100))
        screen.blit(ns, ns.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
        draw_center("ENTER — продолжить", font_small, HEIGHT // 2 + 80)

    # task 3.6: главное меню с кнопками
    elif state == State.MENU:
        draw_overlay()
        draw_center("SNAKE", font_big, HEIGHT // 2 - 80, (100, 255, 100))
        draw_center(f"Привет, {username}!", font_small, HEIGHT // 2 - 28, (180, 180, 180))
        b_play.draw(); b_leader.draw(); b_sett.draw(); b_quit.draw()

    elif state == State.PAUSED:
        draw_overlay()
        draw_center("ПАУЗА", font_big, HEIGHT // 2 - 20)
        draw_center("ПРОБЕЛ — продолжить", font_small, HEIGHT // 2 + 40)

    # task 3.6: game over с очками и кнопками
    elif state == State.GAME_OVER:
        draw_overlay()
        draw_center("ИГРА ОКОНЧЕНА", font_big, HEIGHT // 2 - 100, (255, 80, 80))
        draw_center(f"Очки: {score.current}", font_med, HEIGHT // 2 - 30)
        draw_center(f"Уровень: {score.level}", font_small, HEIGHT // 2 + 15)
        draw_center(f"Личный рекорд: {personal_best}", font_small, HEIGHT // 2 + 45, (180, 255, 180))
        b_retry.draw(); b_tomenu.draw()

    # task 3.6: таблица лидеров
    elif state == State.LEADERBOARD:
        draw_overlay()
        draw_center("ТОП 10", font_big, 55, (255, 215, 0))
        header = font_small.render("#    Игрок               Очки    Ур.   Дата", True, (160, 160, 200))
        screen.blit(header, (30, 108))
        pygame.draw.line(screen, (100, 100, 150), (30, 130), (WIDTH - 30, 130))
        rows = get_top10()
        if rows:
            for i, (uname, sc, lvl, ts) in enumerate(rows):
                line  = f"{i+1:<4} {uname:<20} {sc:<8} {lvl:<5} {ts.strftime('%d.%m.%y')}"
                color = (255, 215, 0) if uname == username else (255, 255, 255)
                screen.blit(font_small.render(line, True, color), (30, 138 + i * 28))
        else:
            draw_center("Пока нет записей", font_small, HEIGHT // 2)
        b_back.draw()

    # task 3.5 + 3.6: экран настроек
    elif state == State.SETTINGS:
        draw_overlay()
        draw_center("НАСТРОЙКИ", font_big, 65, (200, 200, 255))
        # текст кнопки меняется в зависимости от значения
        b_grid.text  = f"Сетка:  {'ВКЛ' if temp_settings['grid_overlay'] else 'ВЫКЛ'}"
        b_sound.text = f"Звук:   {'ВКЛ' if temp_settings['sound'] else 'ВЫКЛ'}"
        b_grid.draw(); b_sound.draw()
        draw_center("Цвет змейки:", font_small, HEIGHT // 2 + 68, (200, 200, 200))
        for i, (bc, (_, rgb)) in enumerate(zip(b_colors, COLOR_OPTIONS)):
            selected = (temp_settings["snake_color"] == list(rgb))
            dot_x = bc.rect.centerx
            # цветная точка над каждой кнопкой, белая рамка если выбрана
            pygame.draw.circle(screen, tuple(rgb), (dot_x, bc.rect.top - 8), 6)
            if selected:
                pygame.draw.circle(screen, (255, 255, 255), (dot_x, bc.rect.top - 8), 6, 2)
            bc.draw()
        b_save.draw()
        draw_center("ESC — выйти без сохранения", font_small, HEIGHT - 18, (120, 120, 120))

    pygame.display.flip()
    clock.tick(snake.speed)

pygame.quit()
