import pygame


class Settings:
    """A class to store all settings"""

    def __init__(self):
        """Initialize the game static settings"""
        # Screen settings
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = 1400
        self.screen_height = 700
        self.ship_speed = 1.3
        self.ship_limit = 2
        # Bullet settings
        self.bullet_speed = 3.0
        self.bullet_width = 5
        self.bullet_height = 18
        self.bullet_color = (0, 255, 0)
        self.bullets_allowed = 3
        # Alien Settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # 1 --> right , -1 --> left
        self.fleet_direction = 1
        # Level Up
        self.speed_up_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
        self.difficulty_easy()
        self.difficulty_medium()
        self.difficulty_hard()

    def initialize_dynamic_settings(self):
        """Initialize settings that change through out the game"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        self.fleet_direction = 1
        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed *= self.speed_up_scale
        self.bullet_speed *= self.speed_up_scale
        self.alien_speed *= self.speed_up_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)

    def difficulty_easy(self):
        self.ship_speed -= 0.5
        self.bullet_speed += 1.5
        self.alien_speed -= 0.5

    def difficulty_medium(self):
        self.ship_speed += 2.5
        self.bullet_speed += 2.5
        self.alien_speed += 2.5

    def difficulty_hard(self):
        self.ship_speed += 3.5
        self.bullet_speed += 3.5
        self.alien_speed += 3.5
