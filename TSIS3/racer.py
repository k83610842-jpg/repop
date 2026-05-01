# racer.py contains all game classes and the main game loop
import pygame, sys, random, time
from pygame.locals import *

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self, speed):
        self.rect.move_ip(0, speed[0])
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.weight = random.choice([1, 3, 5])

    def move(self, speed):
        self.rect.move_ip(0, speed[0])
        if self.rect.top > 600:
            self.reset()

    def reset(self):
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.weight = random.choice([1, 3, 5])

class OilSpill(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("oil.png").convert_alpha()
        self.image = pygame.transform.scale(img, (40, 40))
        self.rect  = self.image.get_rect()
        # here we start oil off screen so it doesnt appear right away
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -200)
        self.spawn_time = time.time() + random.randint(5, 10)

    def move(self, speed):
        # here we wait until spawn time before showing oil on screen
        if time.time() < self.spawn_time:
            return
        self.rect.move_ip(0, speed[0])
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class NitroStrip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("nitro.png").convert_alpha()
        self.image = pygame.transform.scale(img, (40, 40))
        self.rect  = self.image.get_rect()
        # here we start nitro off screen so it doesnt appear right away
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -200)
        self.spawn_time = time.time() + random.randint(8, 15)

    def move(self, speed):
        # here we wait until spawn time before showing nitro on screen
        if time.time() < self.spawn_time:
            return
        self.rect.move_ip(0, speed[0])
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, player_rect, delay=0):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect  = self.image.get_rect()
        # here we start traffic car off screen with a delay so they dont all appear at once
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -200)
        self.spawn_time = time.time() + delay

    def move(self, speed):
        # here we wait until spawn time before showing car on screen
        if time.time() < self.spawn_time:
            return
        self.rect.move_ip(0, speed[0])
        if self.rect.top > 600:
            self.rect.top = -60
            self.rect.centerx = random.randint(40, SCREEN_WIDTH - 40)

class Pothole(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # here we use oil image but smaller size so it looks different from oil spill
        img = pygame.image.load("oil.png").convert_alpha()
        self.image = pygame.transform.scale(img, (25, 25))
        self.rect  = self.image.get_rect()
        # here we start pothole off screen with a delay
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -200)
        self.spawn_time = time.time() + random.randint(10, 20)

    def move(self, speed):
        # here we wait until spawn time before showing pothole on screen
        if time.time() < self.spawn_time:
            return
        self.rect.move_ip(0, speed[0])
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, kind, delay=0):
        super().__init__()
        self.kind = kind
        if kind == "nitro":
            img = pygame.image.load("nitro.png").convert_alpha()
        elif kind == "shield":
            img = pygame.image.load("shield.png").convert_alpha()
        elif kind == "repair":
            img = pygame.image.load("repair.png").convert_alpha()
        self.image = pygame.transform.scale(img, (35, 35))
        self.rect = self.image.get_rect()
        # here we start powerup off screen with a delay so they dont stack up
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -200)
        self.spawn_time = time.time() + delay
        self.active = False

    def move(self, speed):
        # here we wait until spawn time before showing powerup on screen
        if time.time() < self.spawn_time:
            return
        self.active = True
        self.rect.move_ip(0, speed[0])
        # here we reset powerup if it goes off screen or times out after 8 seconds
        if self.rect.top > 600 or (self.active and time.time() - self.spawn_time > 8):
            self.respawn()

    def respawn(self):
        # here we give a random delay before next appearance
        self.rect.top = -200
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -200)
        self.spawn_time = time.time() + random.randint(10, 20)
        self.active = False

class Player(pygame.sprite.Sprite):
    def __init__(self, car_color):
        super().__init__()
        # here we load the correct car image based on color chosen in settings
        if car_color == "red":
            img = pygame.image.load("redcar.png").convert_alpha()
        elif car_color == "green":
            img = pygame.image.load("greencar.png").convert_alpha()
        else:
            img = pygame.image.load("Player.png").convert_alpha()
        self.image = pygame.transform.scale(img, (50, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self, speed=None):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# here we run the game and return final score distance and coins when player dies
def run_game(surface, clock, username, settings):
    font_small = pygame.font.SysFont("Verdana", 20)

    SPEED = [5]
    # here we set how much speed increases per second based on difficulty
    if settings["difficulty"] == "easy":
        speed_inc = 0.2
    elif settings["difficulty"] == "normal":
        speed_inc = 0.5
    else:
        speed_inc = 1.0

    SCORE          = 0
    COIN_COUNT     = 0
    active_powerup = None
    shield_active  = False
    nitro_timer    = 0
    start_time     = time.time()


    background = pygame.image.load("AnimatedStreet.png")

    P1     = Player(settings["car_color"])
    E1     = Enemy()
    C1     = Coin()
    Oil1   = OilSpill()
    Nitro1 = NitroStrip()
    # here we give each traffic car a different delay so they appear one by one
    # here we always spawn 2 traffic cars
    T1 = TrafficCar(P1.rect, delay=5)
    T2 = TrafficCar(P1.rect, delay=10)
    traffic_list = [T1, T2]
    Pot1   = Pothole()
    # here we give each powerup a different delay so they dont appear at same time
    PU_n   = PowerUp("nitro",  delay=15)
    PU_s   = PowerUp("shield", delay=25)
    PU_r   = PowerUp("repair", delay=35)

    enemies     = pygame.sprite.Group(E1)
    coins       = pygame.sprite.Group(C1)
    oils        = pygame.sprite.Group(Oil1)
    nitros      = pygame.sprite.Group(Nitro1)
    traffic     = pygame.sprite.Group(*traffic_list)
    potholes    = pygame.sprite.Group(Pot1)
    powerups    = pygame.sprite.Group(PU_n, PU_s, PU_r)
    all_sprites = pygame.sprite.Group(P1, E1, C1, Oil1, Nitro1, *traffic_list, Pot1, PU_n, PU_s, PU_r)

    INC_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INC_SPEED, 1000)

    while True:
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                # here we increase speed based on difficulty
                SPEED[0] += speed_inc

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        distance    = int((time.time() - start_time) * SPEED[0])
        total_score = SCORE * 10 + COIN_COUNT * 5 + distance

        surface.blit(background, (0, 0))
        surface.blit(font_small.render("Score: "  + str(total_score),    True, BLACK), (10, 10))
        surface.blit(font_small.render("Coins: "  + str(COIN_COUNT),     True, BLACK), (SCREEN_WIDTH - 100, 10))
        surface.blit(font_small.render("Dist: "   + str(distance) + "m", True, BLACK), (10, 35))

        if active_powerup == "nitro":
            t = round(nitro_timer - time.time(), 1)
            surface.blit(font_small.render("NITRO " + str(t) + "s", True, (255, 165, 0)), (10, 55))
        elif active_powerup == "shield":
            surface.blit(font_small.render("SHIELD ON", True, (0, 200, 255)), (10, 55))


        for entity in all_sprites:
            surface.blit(entity.image, entity.rect)
            entity.move(SPEED)

        P1.move()

        if active_powerup == "nitro" and time.time() > nitro_timer:
            SPEED[0] -= 3
            active_powerup = None

        if pygame.sprite.spritecollide(P1, coins, False):
            COIN_COUNT += C1.weight
            C1.reset()
            if COIN_COUNT % 10 == 0:
                SPEED[0] += 1

        # here we check collision only if oil is actually on screen
        if Oil1.rect.top > 0 and pygame.sprite.spritecollide(P1, oils, False):
            SPEED[0] -= 2
            Oil1.spawn_time = time.time() + random.randint(8, 15)
            Oil1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -200)

        # here we check collision only if nitro is actually on screen
        if Nitro1.rect.top > 0 and not active_powerup and pygame.sprite.spritecollide(P1, nitros, False):
            SPEED[0] += 3
            active_powerup = "nitro"
            nitro_timer = time.time() + 3
            Nitro1.spawn_time = time.time() + random.randint(10, 20)
            Nitro1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -200)

        if Pot1.rect.top > 0 and pygame.sprite.spritecollide(P1, potholes, False):
            SPEED[0] -= 1
            Pot1.spawn_time = time.time() + random.randint(10, 20)
            Pot1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -200)

        # here we check collision only for powerups that are actually on screen
        hit_powerup = pygame.sprite.spritecollide(P1, powerups, False)
        if hit_powerup and active_powerup is None:
            pu = hit_powerup[0]
            if not pu.active:
                pass
            elif pu.kind == "nitro":
                SPEED[0] += 3
                active_powerup = "nitro"
                nitro_timer = time.time() + 4
                pu.respawn()
            elif pu.kind == "shield":
                active_powerup = "shield"
                shield_active  = True
                pu.respawn()
            elif pu.kind == "repair":
                Pot1.spawn_time = time.time() + random.randint(10, 20)
                Pot1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -200)
                Oil1.spawn_time = time.time() + random.randint(8, 15)
                Oil1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -200)
                pu.respawn()

        # here we check if player hits traffic car
        if pygame.sprite.spritecollideany(P1, traffic):
            if shield_active:
                shield_active  = False
                active_powerup = None
                for car in traffic:
                    car.rect.center  = (random.randint(40, SCREEN_WIDTH - 40), -200)
                    car.spawn_time   = time.time() + 3
            else:
                if settings["sound"]:
                    pygame.mixer.Sound("crash.wav").play()
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
                    pygame.mixer.Sound("crash.wav").play()
                time.sleep(0.5)
                for entity in all_sprites:
                    entity.kill()
                return total_score, distance, COIN_COUNT

        pygame.display.update()
        clock.tick(60)
