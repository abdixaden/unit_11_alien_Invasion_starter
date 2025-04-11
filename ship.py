import pygame
from typing import TYPE_CHECKING
from arsenal import Arsenal

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Ship:
    def __init__(self, game: "AlienInvasion", arsenal: 'Arsenal'):
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()
        
        self.image = pygame.image.load(str(self.settings.ship_file))
        self.image = pygame.transform.scale(self.image, 
                                            (self.settings.ship_w, self.settings.ship_h))
        
        self.rect = self.image.get_rect()
        self.rect.midright = self.boundaries.midright  # Ship positioned at the right edge
        
        self.ship_speed = 5.0
        self.moving_right = False
        self.moving_left = False
        self.x = float(self.rect.x)
        self.arsenal = arsenal
    
    def update(self):   
        if self.moving_right and not self.moving_left:
            self.x += self.settings.ship_speed
        elif self.moving_left and not self.moving_right:
            self.x -= self.settings.ship_speed
        self.rect.x = int(self.x)
        
        self.arsenal.update_arsenal()
        
    def center_ship(self):
        self.rect.midright = self.boundaries.midright  # Keep ship at the right edge
        self.x = float(self.rect.x)

    def draw(self):
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)
        
    def fire(self):
        return self.arsenal.fire_bullet()  # arsenal.py
