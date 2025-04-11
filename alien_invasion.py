import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from arsenal import Arsenal
from alien import Alien
from game_stats import GameStats

class AlienInvasion:
    
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        
        # Create the screen
        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h))
        pygame.display.set_caption(self.settings.name)
        
        # Create GameStats
        self.stats = GameStats(self)
        
        # Background setup
        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg,
                                         (self.settings.screen_w, self.settings.screen_h))
        
        self.running = True
        self.game_active = True  
        self.clock = pygame.time.Clock()
        
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)
        
        self.ship = Ship(self, Arsenal(self))
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        
    def _create_fleet(self):
        """Create the fleet of aliens horizontally."""
        alien = Alien(self)
        alien_width = alien.rect.width  # Use rect width directly
        alien_height = alien.rect.height  # Use rect height directly
        
        # Determine the number of aliens that fit on the screen horizontally
        available_space_x = self.settings.screen_w - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        # Create the fleet of aliens
        for alien_number in range(number_aliens_x):
            self._create_alien(alien_number)
    
    def _create_alien(self, alien_number):
        """Create an alien and place it on the screen horizontally."""
        alien = Alien(self)
        alien_width = alien.rect.width  # Use rect width directly
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
    
    # Use a fixed value for the Y-position of aliens
        alien.rect.y = 100  # Hard-coded value for where to place aliens on the screen
        self.aliens.add(alien)

        
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
                
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()
        
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            
        # Check for aliens hitting the right edge of the screen
        self._check_aliens_reached_right_edge()
        
    def _check_aliens_reached_right_edge(self):
        """Check if any aliens have reached the right edge of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.right >= screen_rect.right:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break
                
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1
            
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.ship.arsenal.arsenal.empty()
            
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            
            # Pause for a brief moment
            sleep(0.5)
        else:
            self.game_active = False 
    
    def reset_game(self):
        """Reset the game settings to start a new game."""
        self.stats.reset_stats()
        self.game_active = True
        self._create_fleet()
        self.ship.center_ship()
        
    def run_game(self):
        while self.running:
            self._check_events()       
            self._update_screen()
            self.ship.update()
            self.clock.tick(self.settings.FPS)
            
    def _update_bullets(self):
     """Update the position of bullets and check for collisions."""
     # Update bullets
     self.ship.arsenal.update_arsenal()

     # Check for collisions between bullets and aliens
     collisions = pygame.sprite.groupcollide(
         self.ship.arsenal.arsenal, self.aliens, True, True)

     # If all aliens are destroyed, create a new fleet
     if not self.aliens:
         self.ship.arsenal.arsenal.empty()
         self._create_fleet()


    def _update_screen(self):
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        self.aliens.draw(self.screen)
        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                
    def _check_keydown_events(self, event):
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(250)
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
