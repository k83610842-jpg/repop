import pygame
import random
import os

# Настройки экрана и сетки
pygame.init()
TILE = 20
COLS, ROWS = 30, 30
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE + 40  # Оставили место сверху под счетчик
GRID_TOP = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка с уровнями")
clock = pygame.time.Clock()
font_big = pygame.font.SysFont("Verdana", 48)
font_small = pygame.font.SysFont("Verdana", 20)

HIGHSCORE_FILE = "highscore.txt"

# Состояния игры
class State:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

# Управляем очками и уровнями
class ScoreManager:
    def __init__(self, path=HIGHSCORE_FILE):
        self.path = path
        self.current = 0
        self.level = 1 # Добавили текущий уровень
        self.high = self._load()

    # Грузим рекорд из файла
    def _load(self):
        if not os.path.exists(self.path):
            return 0
        try:
            with open(self.path) as f:
                return int(f.read().strip() or 0)
        except ValueError:
            return 0

    # Сохраняем новый рекорд
    def _save(self):
        with open(self.path, "w") as f:
            f.write(str(self.high))

    # Добавляем очки и проверяем рекорд
    def add(self, points):
        self.current += points
        if self.current > self.high:
            self.high = self.current
            self._save()

    # Сброс при новой игре
    def reset(self):
        self.current = 0
        self.level = 1

# Класс змейки
class Snake:
    def __init__(self):
        self.reset()

    # Начальные настройки змейки
    def reset(self):
        self.body = [[15, 15]]
        self.dx, self.dy = 1, 0
        self.grow = False
        self.speed = 8 # Начальная скорость

    # Двигаем хвост за головой
    def move(self):
        if self.grow:
            self.body.append(list(self.body[-1]))
            self.grow = False
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i][0] = self.body[i - 1][0]
            self.body[i][1] = self.body[i - 1][1]
        self.body[0][0] += self.dx
        self.body[0][1] += self.dy

    def head(self):
        return self.body[0]

    # Проверка не врезались ли в себя
    def hits_self(self):
        return self.body[0] in self.body[1:]

    # Проверка не вылетели ли за границы экрана
    def hits_wall(self):
        c, r = self.body[0]
        return c < 0 or c >= COLS or r < 0 or r >= ROWS

    # Рисуем голову и тело разными цветами
    def draw(self):
        for i, (c, r) in enumerate(self.body):
            color = (0, 220, 0) if i == 0 else (0, 170, 0)
            pygame.draw.rect(
                screen, color,
                pygame.Rect(c * TILE, GRID_TOP + r * TILE, TILE, TILE),
            )

# --- TASK 1 & 2: Extended Food class with multiple types and disappearing timer ---

# Таблица типов еды: каждый тип имеет вес (очки), цвет и время жизни в секундах
# lifetime=None означает что еда не исчезает (обычная еда)
FOOD_TYPES = [
    {"points": 1,  "color": (220, 60,  60),  "lifetime": None},  # Обычная красная — не исчезает
    {"points": 3,  "color": (255, 165,  0),  "lifetime": 7},     # Оранжевая — исчезает через 7 сек
    {"points": 5,  "color": (255, 215,  0),  "lifetime": 5},     # Золотая — исчезает через 5 сек
    {"points": 10, "color": (180,  0,  255), "lifetime": 3},     # Фиолетовая — исчезает через 3 сек
]

# Вероятности появления каждого типа еды (должны суммироваться в 1.0)
FOOD_WEIGHTS = [0.50, 0.25, 0.15, 0.10]

class Food:
    def __init__(self):
        self.c, self.r = 10, 10
        self.points = 1
        self.color = (220, 60, 60)
        self.lifetime = None   # None = не исчезает; число = секунды до исчезновения
        self.spawn_time = None # Время появления еды (pygame.time.get_ticks())

    # Появляем еду так чтобы она не попала на змейку
    def respawn(self, blocked):
        while True:
            self.c = random.randint(0, COLS - 1)
            self.r = random.randint(0, ROWS - 1)
            if [self.c, self.r] not in blocked:
                break

        # Случайно выбираем тип еды согласно заданным весам (TASK 1)
        chosen = random.choices(FOOD_TYPES, weights=FOOD_WEIGHTS, k=1)[0]
        self.points     = chosen["points"]
        self.color      = chosen["color"]
        self.lifetime   = chosen["lifetime"]
        self.spawn_time = pygame.time.get_ticks()  # Запоминаем момент появления (TASK 2)

    # Проверяем не истекло ли время жизни еды (TASK 2)
    # Возвращает True если еда должна исчезнуть
    def is_expired(self):
        if self.lifetime is None:
            return False  # Обычная еда никогда не исчезает
        elapsed = (pygame.time.get_ticks() - self.spawn_time) / 1000  # Прошло секунд
        return elapsed >= self.lifetime

    # Возвращает оставшееся время жизни еды в секундах (для отображения)
    def time_left(self):
        if self.lifetime is None:
            return None
        elapsed = (pygame.time.get_ticks() - self.spawn_time) / 1000
        return max(0, self.lifetime - elapsed)

    def draw(self):
        pygame.draw.rect(
            screen, self.color,
            pygame.Rect(self.c * TILE, GRID_TOP + self.r * TILE, TILE, TILE),
        )
        # Рисуем таймер над едой если у неё есть время жизни (TASK 2)
        tl = self.time_left()
        if tl is not None:
            # Мигаем когда остаётся меньше 2 секунд (чётные десятые секунды — видно, нечётные — скрыто)
            if tl > 2 or int(tl * 2) % 2 == 0:
                timer_surf = font_small.render(str(int(tl) + 1), True, (255, 255, 255))
                screen.blit(timer_surf, (self.c * TILE, GRID_TOP + self.r * TILE - 18))

# Клетчатый фон
def draw_background():
    pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(0, 0, WIDTH, GRID_TOP))
    colors = [(30, 30, 30), (40, 40, 40)]
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(
                screen, colors[(r + c) % 2],
                pygame.Rect(c * TILE, GRID_TOP + r * TILE, TILE, TILE),
            )

# Рисуем счет уровень и рекорд наверху
def draw_hud(score):
    s = font_small.render(f"Очки: {score.current}", True, (255, 255, 255))
    l = font_small.render(f"Уровень: {score.level}", True, (100, 200, 255))
    h = font_small.render(f"Рекорд: {score.high}", True, (255, 215, 0))
    screen.blit(s, (10, 8))
    screen.blit(l, (WIDTH // 2 - l.get_width() // 2, 8))
    screen.blit(h, (WIDTH - h.get_width() - 10, 8))

# Удобная функция чтобы текст был по центру
def draw_center(text, font, y, color=(255, 255, 255)):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, y))
    screen.blit(surf, rect)

# Создаем объекты
snake = Snake()
food = Food()
food.respawn(snake.body)  # Сразу спавним еду чтобы spawn_time был инициализирован
score = ScoreManager()
state = State.MENU

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if state == State.MENU and event.key == pygame.K_RETURN:
                state = State.PLAYING
            elif state == State.PLAYING:
                if event.key == pygame.K_SPACE:
                    state = State.PAUSED
                # Проверка чтобы змейка не могла развернуться на 180 градусов
                elif event.key == pygame.K_RIGHT and snake.dx != -1:
                    snake.dx, snake.dy = 1, 0
                elif event.key == pygame.K_LEFT and snake.dx != 1:
                    snake.dx, snake.dy = -1, 0
                elif event.key == pygame.K_UP and snake.dy != 1:
                    snake.dx, snake.dy = 0, -1
                elif event.key == pygame.K_DOWN and snake.dy != -1:
                    snake.dx, snake.dy = 0, 1
            elif state == State.PAUSED and event.key == pygame.K_SPACE:
                state = State.PLAYING
            elif state == State.GAME_OVER and event.key == pygame.K_RETURN:
                snake.reset()
                score.reset()
                food.respawn(snake.body)
                state = State.PLAYING

    if state == State.PLAYING:
        snake.move()
        
        # Если врезались в стену или в себя то конец игры
        if snake.hits_wall() or snake.hits_self():
            state = State.GAME_OVER
        
        # Если съели еду
        elif snake.head() == [food.c, food.r]:
            snake.grow = True
            score.add(food.points)
            
            # Логика уровней: каждые 5 очков уровень растет и скорость увеличивается
            if score.current // 5 >= score.level:
                score.level += 1
                snake.speed += 2
                
            food.respawn(snake.body)

        # Проверяем не истекло ли время жизни еды (TASK 2)
        # Если истекло — спавним новую еду без начисления очков
        elif food.is_expired():
            food.respawn(snake.body)

    # Рисуем всё на экран
    draw_background()
    food.draw()
    snake.draw()
    draw_hud(score)
    # Тексты для разных экранов
    if state == State.MENU:
        draw_center("SNAKE", font_big, HEIGHT // 2 - 40)
        draw_center("PRESS ENTER TO START", font_small, HEIGHT // 2 + 20)
    elif state == State.PAUSED:
        draw_center("PAUSE", font_big, HEIGHT // 2 - 20)
        draw_center("PRESS ПРОБЕЛ TO CONTINUE", font_small, HEIGHT // 2 + 30)
    elif state == State.GAME_OVER:
        draw_center("LOSER", font_big, HEIGHT // 2 - 60)
        draw_center(f"YOUR SCORE: {score.current}", font_small, HEIGHT // 2)
        draw_center(f"MAX SCORE: {score.level}", font_small, HEIGHT // 2 + 30)
        draw_center("PRESS ENTER TO START", font_small, HEIGHT // 2 + 80)
    pygame.display.flip()
    clock.tick(snake.speed)
pygame.quit()