import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    # 12.2
    """A class to manage the alien"""
    def __init__(self, ai):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai.screen
        self.settings = ai.settings
        # Load the ship image and get its rect
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw thw ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the alien to right or left"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return true if alien is at edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <=0:
            return True


