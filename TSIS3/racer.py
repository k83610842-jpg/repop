# racer.py contains all game classes and the main game loop
import pygame, sys, random, time
from pygame.locals import *

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600

BLUE   = (0, 0, 255)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)

font_small = pygame.font.SysFont("Verdana", 20)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Enemy.png")
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self, speed_ref):
        self.rect.move_ip(0, speed_ref[0])
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            return 1  # here we return 1 to add to score
        return 0

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/coin.png")
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        # here we give each coin a random weight
        self.weight = random.choice([1, 3, 5])

    def move(self, speed_ref):
        self.rect.move_ip(0, speed_ref[0])
        if self.rect.top > 600:
            self.reset()

    def reset(self):
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.weight = random.choice([1, 3, 5])

class OilSpill(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # here we draw a dark ellipse to represent oil spill
        self.image = pygame.Surface((50, 25), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (30, 30, 30), (0, 0, 50, 25))
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self, speed_ref):
        self.rect.move_ip(0, speed_ref[0])
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class NitroStrip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # here we draw a yellow rectangle to represent nitro strip
        self.image = pygame.Surface((60, 15))
        self.image.fill((255, 255, 0))
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self, speed_ref):
        self.rect.move_ip(0, speed_ref[0])
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        # here we draw a blue rectangle as traffic car
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 100, 255))
        self.rect  = self.image.get_rect()
        self.rect.center = self.safe_spawn(player_rect)

    def safe_spawn(self, player_rect):
        # here we make sure car does not spawn on top of player
        for _ in range(20):
            x = random.randint(40, SCREEN_WIDTH - 40)
            y = random.randint(-200, -50)
            if abs(x - player_rect.centerx) > 60:
                return (x, y)
        return (random.randint(40, SCREEN_WIDTH - 40), -100)

    def move(self, speed_ref):
        self.rect.move_ip(0, speed_ref[0])
        if self.rect.top > 600:
            self.rect.top = -60
            self.rect.centerx = random.randint(40, SCREEN_WIDTH - 40)

class Pothole(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # here we draw a brown circle to represent pothole
        self.image = pygame.Surface((35, 35), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (101, 67, 33), (17, 17), 17)
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self, speed_ref):
        self.rect.move_ip(0, speed_ref[0])
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, kind):
        super().__init__()
        self.kind  = kind
        self.image = pygame.Surface((30, 30))
        # here we set color based on powerup type
        if kind == "nitro":
            self.image.fill((255, 165, 0))
        elif kind == "shield":
            self.image.fill((0, 200, 255))
        elif kind == "repair":
            self.image.fill((0, 220, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.spawn_time = time.time()

    def move(self, speed_ref):
        self.rect.move_ip(0, speed_ref[0])
        # here we reset powerup if it goes off screen or times out after 8 seconds
        if self.rect.top > 600 or time.time() - self.spawn_time > 8:
            self.respawn()

    def respawn(self):
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.spawn_time = time.time()

class Player(pygame.sprite.Sprite):
    def __init__(self, car_color):
        super().__init__()
        self.image = pygame.image.load("assets/Player.png")
        # here we apply car color from settings
        if car_color != "red":
            color_map = {"blue": BLUE, "green": GREEN, "yellow": (255, 255, 0)}
            self.image.fill(color_map.get(car_color, RED))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self, speed_ref=None):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# here we run the game and return final score distance and coins when player dies
def run_game(surface, clock, username, settings):
    SPEED = [5]  # here we use a list so all classes can share the same speed value
    if settings["difficulty"] == "easy":
        SPEED[0] = 3
    elif settings["difficulty"] == "hard":
        SPEED[0] = 7

    SCORE         = 0
    COIN_COUNT    = 0
    active_powerup = None
    shield_active  = False
    nitro_timer    = 0
    difficulty     = 1
    start_time     = time.time()

    background = pygame.image.load("assets/AnimatedStreet.png")

    P1     = Player(settings["car_color"])
    E1     = Enemy()
    C1     = Coin()
    Oil1   = OilSpill()
    Nitro1 = NitroStrip()
    T1     = TrafficCar(P1.rect)
    T2     = TrafficCar(P1.rect)
    Pot1   = Pothole()
    PU_n   = PowerUp("nitro")
    PU_s   = PowerUp("shield")
    PU_r   = PowerUp("repair")

    enemies     = pygame.sprite.Group(E1)
    coins       = pygame.sprite.Group(C1)
    oils        = pygame.sprite.Group(Oil1)
    nitros      = pygame.sprite.Group(Nitro1)
    traffic     = pygame.sprite.Group(T1, T2)
    potholes    = pygame.sprite.Group(Pot1)
    powerups    = pygame.sprite.Group(PU_n, PU_s, PU_r)
    all_sprites = pygame.sprite.Group(P1, E1, C1, Oil1, Nitro1, T1, T2, Pot1, PU_n, PU_s, PU_r)

    INC_SPEED      = pygame.USEREVENT + 1
    INC_DIFFICULTY = pygame.USEREVENT + 2
    pygame.time.set_timer(INC_SPEED,      1000)
    pygame.time.set_timer(INC_DIFFICULTY, 10000)

    while True:
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                SPEED[0] += 0.5
            if event.type == INC_DIFFICULTY:
                # here we add one more traffic car every 10 seconds
                difficulty += 1
                new_car = TrafficCar(P1.rect)
                traffic.add(new_car)
                all_sprites.add(new_car)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        distance    = int((time.time() - start_time) * SPEED[0])
        total_score = SCORE * 10 + COIN_COUNT * 5 + distance

        surface.blit(background, (0, 0))

        surface.blit(font_small.render("Score: "  + str(total_score),        True, BLACK), (10, 10))
        surface.blit(font_small.render("Coins: "  + str(COIN_COUNT),         True, BLACK), (SCREEN_WIDTH - 100, 10))
        surface.blit(font_small.render("Dist: "   + str(distance) + "m",     True, BLACK), (10, 35))
        surface.blit(font_small.render("Lvl: "    + str(difficulty),         True, BLACK), (SCREEN_WIDTH - 70, 35))

        if active_powerup == "nitro":
            t = round(nitro_timer - time.time(), 1)
            surface.blit(font_small.render("NITRO " + str(t) + "s", True, (255, 165, 0)), (10, 55))
        elif active_powerup == "shield":
            surface.blit(font_small.render("SHIELD ON", True, (0, 200, 255)), (10, 55))

        for entity in all_sprites:
            surface.blit(entity.image, entity.rect)
            entity.move(SPEED)

        # here we fix enemy score counting since move returns 1 when enemy passes
        SCORE += E1.move(SPEED) or 0

        if active_powerup == "nitro" and time.time() > nitro_timer:
            SPEED[0] -= 3
            active_powerup = None

        if pygame.sprite.spritecollide(P1, coins, False):
            COIN_COUNT += C1.weight
            C1.reset()
            if COIN_COUNT % 10 == 0:
                SPEED[0] += 1

        if pygame.sprite.spritecollide(P1, oils, False):
            SPEED[0] -= 2
            Oil1.rect.top = 0
            Oil1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

        if not active_powerup and pygame.sprite.spritecollide(P1, nitros, False):
            SPEED[0] += 3
            active_powerup = "nitro"
            nitro_timer = time.time() + 3
            Nitro1.rect.top = 0
            Nitro1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

        if pygame.sprite.spritecollide(P1, potholes, False):
            SPEED[0] -= 1
            Pot1.rect.top = 0
            Pot1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

        hit_powerup = pygame.sprite.spritecollide(P1, powerups, False)
        if hit_powerup and active_powerup is None:
            pu = hit_powerup[0]
            if pu.kind == "nitro":
                SPEED[0] += 3
                active_powerup = "nitro"
                nitro_timer = time.time() + 4
            elif pu.kind == "shield":
                active_powerup = "shield"
                shield_active  = True
            elif pu.kind == "repair":
                Pot1.rect.top = 0
                Pot1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
                Oil1.rect.top = 0
                Oil1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            pu.respawn()

        # here we check if player hits traffic car
        if pygame.sprite.spritecollideany(P1, traffic):
            if shield_active:
                shield_active  = False
                active_powerup = None
                for car in traffic:
                    car.rect.top     = -100
                    car.rect.centerx = random.randint(40, SCREEN_WIDTH - 40)
            else:
                if settings["sound"]:
                    pygame.mixer.Sound("assets/crash.wav").play()
                time.sleep(0.5)
                for entity in all_sprites:
                    entity.kill()
                return total_score, distance, COIN_COUNT

        # here we check if player hits enemy
        if pygame.sprite.spritecollideany(P1, enemies):
            if shield_active:
                shield_active  = False
                active_powerup = None
                E1.rect.top    = 0
                E1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            else:
                if settings["sound"]:
                    pygame.mixer.Sound("assets/crash.wav").play()
                time.sleep(0.5)
                for entity in all_sprites:
                    entity.kill()
                return total_score, distance, COIN_COUNT

        pygame.display.update()
        clock.tick(60)