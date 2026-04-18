import pygame
class Ball:
    def __init__(self,w,h):
        self.r=25
        self.color=(255,0,0)
        self.x=w//2
        self.y=h//2
        self.step=1
        self.w=w
        self.h=h
    def move(self,direction):
        if direction=="UP" and self.y-self.step>=self.r:
            self.y-=self.step
        elif direction=="DOWN" and self.y+self.step<=self.h-self.r:
            self.y+=self.step
        elif direction=="LEFT" and self.x-self.step>=self.r:
            self.x-=self.step
        elif direction=="RIGHT" and self.x+self.step<=self.w-self.r:
            self.x+=self.step
    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.r)
