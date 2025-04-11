# bullet.py
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        
        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(
            self.image,
            (self.settings.bullet_w, self.settings.bullet_h) )
        
        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop
        self.y = float(self.rect.y)
            
    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
                 
    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)
        
        