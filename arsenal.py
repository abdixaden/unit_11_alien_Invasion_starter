
import pygame
from pygame.sprite import Group
from bullet import Bullet

class Arsenal:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.arsenal = Group()
        
    def update_arsenal(self):
        self.arsenal.update()
        self._remove_bullets_offscreen()
        
        
    def _remove_bullets_offscreen(self):
        for bullet in self.arsenal.copy():
            if bullet.rect.bottom <=0:
                self.arsenal.remove(bullet)
        
    def draw(self):
        for bullet in self.arsenal:
            bullet.draw_bullet()
            
    def fire_bullet(self):
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False
    
    def draw(self):
        """Draw bullets to the screen."""
        for bullet in self.arsenal:
            bullet.draw_bullet()