import sys
import time
import pygame
from ai_settings import Settings
from ship import Ship
from alien import Alien
from bullet import Bullet
from time import sleep
from ai_stats import GameStats
from button import Button, Sign, DButton
from ai_scoreboard import Scoreboard


class AlienInvasion:
    """Overall Class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # stats instance
        self.stats = GameStats(self)
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        # Instance of Scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # Background Color
        self.galaxy = pygame.image.load('images/galaxy.jpg')
        self.rect = self.galaxy.get_rect()
        # Bullets
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # Make the play button
        self.play_button = Button(self, "Play")
        self.sign = Sign(self, "Developer : Mastermindx33")
        # Difficulty button
        # self.difficulty_button = DButton(self, "Levels")
        # Sounds
        self.bulletSound = pygame.mixer.Sound("Sounds/gun.mp3")
        # self.hitSound = pygame.mixer.Sound("hit.wav")
        self.music = pygame.mixer.music.load("Sounds/l.mp3")
        pygame.mixer.music.play(-1)

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self.glit()
            self._check_events()
            if self.stats.game:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Respond to key press and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._close_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game:
            self._start_game()

    def _check_keydown_events(self, event):
        """Response to key presses"""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
        if event.key == pygame.K_p:
            self.stats.game = True
        if event.key == pygame.K_LEFT:
            # Move the ship to the left
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._close_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.stats.game:
            self._start_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            # Move the ship to the left
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bulletSound.play()
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """update images on the screen and flip to the new screen"""
        # BgColor
        # 12.1
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        #  Draw score
        self.sb.show_score()
        # Draw the play button if the game is inactive
        if not self.stats.game:
            self.play_button.draw_button()
            self.sign.draw_button()
        # if not self.stats.game:
        #     self.difficulty_button.draw_button()
        pygame.display.flip()

    def _update_bullets(self):
        # To get rid of used bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_collisions()

    def _check_ship_collision(self):
        # To look for alien ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _check_collisions(self):
        # Check for any bullets , that have hit the alien
        # If so get rid of the bullet and the alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _start_game(self):
        """Start a new game."""
        # Reset the game settings.
        self.settings.initialize_dynamic_settings()

        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _update_aliens(self):
        """Check if fleet is at the edge"""
        self._check_fleet_edges()
        self.aliens.update()
        self._check_ship_collision()
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Make a alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create a full fleet of alien
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # Create an alien and place it in the row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _ship_hit(self):
        """Respond to the ship hit by alien"""
        if self.stats.ships_left > 0:
            # Decrement ships left, update score board
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # pause
            sleep(1)
        else:
            self.stats.game = False
            pygame.mouse.set_visible(True)
        # Get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

    def glit(self):
        # Load Galaxy
        self.screen.blit(self.galaxy, (0, 0))

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_directions()
                break

    def _change_fleet_directions(self):
        """Drop the entire fleet and change the direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _close_game(self):
        """Save high score and exit."""
        self.stats.get_high_score()
        with open('high_score.txt', 'w') as hw:
            # print("JSON 755")
            hw.write(str(self.stats.high_score))
            time.sleep(1)
            sys.exit()


if __name__ == '__main__':
    # make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
