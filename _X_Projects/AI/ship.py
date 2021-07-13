import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship"""

    def __init__(self, ai):
        super().__init__()

        """Initialize the ship and set its starting position"""
        self.screen = ai.screen
        self.screen_rect = ai.screen.get_rect()
        self.settings = ai.settings
        # Load the ship image and get its rect
        self.image = pygame.image.load('Images/ship.png')
        self.rect = self.image.get_rect()
        # Start new ship at te centre of bottom
        self.rect.midbottom = self.screen_rect.midbottom
        # Decimal value to ship's horizontal position
        self.x = float(self.rect.x)
        # Movement Flag
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """Update the ship's position based on movement flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
