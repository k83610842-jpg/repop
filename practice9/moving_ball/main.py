import pygame 
import sys
from m1 import Ball
def main():
    pygame.init()
    W,H=600,400
    screen=pygame.display.set_mode((W,H))
    pygame.display.set_caption("moving ball game")
    ball=Ball(W,H)
    clock=pygame.time.Clock()
    running=True
    while running:
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            ball.move("UP")
        if keys[pygame.K_DOWN]:
            ball.move("DOWN")
        if keys[pygame.K_LEFT]:
            ball.move("LEFT")
        if keys[pygame.K_RIGHT]:
            ball.move("RIGHT")
        ball.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()
if __name__=="__main__":
    main()
