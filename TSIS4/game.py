
# тут все игровые классы змейка, еда, яд, пауэрапы, препятствия

import pygame
import random
import os
import json

from config import (
    TILE, COLS, ROWS, GRID_TOP,
    HIGHSCORE_FILE, SETTINGS_FILE, DEFAULT_SETTINGS,
    FOOD_TYPES, FOOD_WEIGHTS, POWERUP_TYPES,
)


#  task 3.5: загрузка и сохранение настроек 

def load_settings():
    # открываю файл и читаю json, если файла нет возвращаю дефолтные
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE) as f:
                data = json.load(f)
            # если вдруг какого-то ключа нет добавляю дефолтное значение
            for k, v in DEFAULT_SETTINGS.items():
                data.setdefault(k, v)
            return data
        except Exception:
            pass
    return dict(DEFAULT_SETTINGS)

def save_settings(s):
    # просто записываю словарь в json файл
    with open(SETTINGS_FILE, "w") as f:
        json.dump(s, f, indent=2)


# счёт и уровень

class ScoreManager:
    def __init__(self):
        self.current = 0
        self.level   = 1
        self.high    = self._load()  # загружаю рекорд из файла при старте

    def _load(self):
        if not os.path.exists(HIGHSCORE_FILE):
            return 0
        try:
            with open(HIGHSCORE_FILE) as f:
                return int(f.read().strip() or 0)
        except ValueError:
            return 0

    def _save(self):
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(self.high))

    def add(self, points):
        self.current += points
        # если побили рекорд сразу сохраняем
        if self.current > self.high:
            self.high = self.current
            self._save()

    def reset(self):
        self.current = 0
        self.level   = 1


# змейка

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body        = [[15, 15]]  # начинаем с одного сегмента в центре
        self.dx, self.dy = 1, 0        # изначально двигается вправо
        self.grow        = False
        self.speed       = 8

    def move(self):
        # если нужно вырасти — добавляем сегмент в конец
        if self.grow:
            self.body.append(list(self.body[-1]))
            self.grow = False
        # двигаем каждый сегмент на позицию предыдущего
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i][0] = self.body[i-1][0]
            self.body[i][1] = self.body[i-1][1]
        # двигаем голову
        self.body[0][0] += self.dx
        self.body[0][1] += self.dy

    def head(self):
        return self.body[0]

    def hits_self(self):
        # голова попала на свой же сегмент
        return self.body[0] in self.body[1:]

    def hits_wall(self):
        c, r = self.body[0]
        return c < 0 or c >= COLS or r < 0 or r >= ROWS

    def draw(self, screen, font_small, settings):
        # цвет берём из настроек (task 3.5), тело делаем чуть темнее головы
        head_col = tuple(settings["snake_color"])
        body_col = tuple(max(0, v - 50) for v in head_col)
        for i, (c, r) in enumerate(self.body):
            col = head_col if i == 0 else body_col
            pygame.draw.rect(screen, col,
                pygame.Rect(c * TILE, GRID_TOP + r * TILE, TILE, TILE))


# --- обычная еда ---

class Food:
    def __init__(self):
        self.c = self.r = 0
        self.points     = 1
        self.color      = (220, 60, 60)
        self.lifetime   = None   # None = не исчезает
        self.spawn_time = None

    def respawn(self, blocked):
        # ищем свободную клетку — не на змейке и не на препятствиях
        while True:
            self.c = random.randint(0, COLS - 1)
            self.r = random.randint(0, ROWS - 1)
            if [self.c, self.r] not in blocked:
                break
        # выбираем случайный тип еды с учётом весов
        chosen          = random.choices(FOOD_TYPES, weights=FOOD_WEIGHTS, k=1)[0]
        self.points     = chosen["points"]
        self.color      = chosen["color"]
        self.lifetime   = chosen["lifetime"]
        self.spawn_time = pygame.time.get_ticks()

    def is_expired(self):
        if self.lifetime is None:
            return False
        return (pygame.time.get_ticks() - self.spawn_time) / 1000 >= self.lifetime

    def time_left(self):
        if self.lifetime is None:
            return None
        return max(0, self.lifetime - (pygame.time.get_ticks() - self.spawn_time) / 1000)

    def draw(self, screen, font_small):
        pygame.draw.rect(screen, self.color,
            pygame.Rect(self.c * TILE, GRID_TOP + self.r * TILE, TILE, TILE))
        # если еда исчезает — показываем таймер над ней, мигает когда < 2 сек
        tl = self.time_left()
        if tl is not None and (tl > 2 or int(tl * 2) % 2 == 0):
            screen.blit(font_small.render(str(int(tl) + 1), True, (255, 255, 255)),
                        (self.c * TILE, GRID_TOP + self.r * TILE - 18))


# --- ядовитая еда ---

class PoisonFood:
    def __init__(self):
        self.c = self.r = -1
        self.active     = False  # не активна пока не заспавнилась
        self.spawn_time = None
        self.lifetime   = 8      # висит 8 секунд и исчезает

    def respawn(self, blocked):
        while True:
            self.c = random.randint(0, COLS - 1)
            self.r = random.randint(0, ROWS - 1)
            if [self.c, self.r] not in blocked:
                break
        self.active     = True
        self.spawn_time = pygame.time.get_ticks()

    def is_expired(self):
        if not self.active:
            return False
        return (pygame.time.get_ticks() - self.spawn_time) / 1000 >= self.lifetime

    def draw(self, screen, font_small):
        if not self.active:
            return
        pygame.draw.rect(screen, (120, 0, 0),
            pygame.Rect(self.c * TILE, GRID_TOP + self.r * TILE, TILE, TILE))
        # рисую крестик чтоб было видно что яд
        screen.blit(font_small.render("X", True, (255, 60, 60)),
                    (self.c * TILE + 2, GRID_TOP + self.r * TILE))


# --- пауэрапы ---

class PowerUp:
    def __init__(self):
        self.c = self.r     = -1
        self.active         = False
        self.spawn_time     = None
        self.field_lifetime = 8   # лежит на поле 8 секунд
        self.kind  = None
        self.color = (255, 255, 255)
        self.label = "?"

    def respawn(self, blocked):
        while True:
            self.c = random.randint(0, COLS - 1)
            self.r = random.randint(0, ROWS - 1)
            if [self.c, self.r] not in blocked:
                break
        # случайно выбираем один из трёх видов
        chosen     = random.choice(POWERUP_TYPES)
        self.kind  = chosen["kind"]
        self.color = chosen["color"]
        self.label = chosen["label"]
        self.active     = True
        self.spawn_time = pygame.time.get_ticks()

    def is_expired(self):
        if not self.active:
            return False
        return (pygame.time.get_ticks() - self.spawn_time) / 1000 >= self.field_lifetime

    def draw(self, screen, font_small):
        if not self.active:
            return
        pygame.draw.rect(screen, self.color,
            pygame.Rect(self.c * TILE, GRID_TOP + self.r * TILE, TILE, TILE))
        screen.blit(font_small.render(self.label, True, (0, 0, 0)),
                    (self.c * TILE + 3, GRID_TOP + self.r * TILE + 1))


# --- task 3.4: препятствия ---

class Obstacles:
    def __init__(self):
        self.blocks = []  # список координат всех блоков

    def generate(self, level, snake_body):
        self.blocks = []
        if level < 3:
            return  # до 3 уровня препятствий нет вообще

        # с каждым уровнем блоков становится больше, но не больше 20
        count = min((level - 2) * 3, 20)

        # зона рядом со змейкой — туда не ставим блоки чтобы не убить сразу
        hc, hr = snake_body[0]
        safe = {(hc + dc, hr + dr) for dc in range(-3, 4) for dr in range(-3, 4)}

        attempts = 0
        while len(self.blocks) < count and attempts < 1000:
            attempts += 1
            c = random.randint(0, COLS - 1)
            r = random.randint(0, ROWS - 1)
            if (c, r) in safe:
                continue
            if [c, r] in snake_body or [c, r] in self.blocks:
                continue
            self.blocks.append([c, r])

    def hits(self, pos):
        # проверяем столкнулась ли голова с блоком
        return pos in self.blocks

    def draw(self, screen):
        for (c, r) in self.blocks:
            pygame.draw.rect(screen, (100, 100, 120),
                pygame.Rect(c * TILE, GRID_TOP + r * TILE, TILE, TILE))
            # рамка чтоб блоки выглядели как стены
            pygame.draw.rect(screen, (60, 60, 80),
                pygame.Rect(c * TILE, GRID_TOP + r * TILE, TILE, TILE), 2)
