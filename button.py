import pygame.font
class Button:

    def __init__(self, ai, msg):
        """Initialize button attributes"""
        self.screen = ai.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 200, 50
        # self.button_color = (0, 185, 0)
        self.text_color = (0, 215, 165)
        self.font = pygame.font.Font("Font/fonts.ttf", 48)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx += 540
        self.rect.centery += 410

        # The button message needs to be prepped once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect(center=(self.width / 2, self.height / 2))
        self.msg_image_rect.centerx += 540
        self.msg_image_rect.centery += 405

    def draw_button(self):
        # Draw blank button then draw message
        self.screen.blit(self.msg_image, self.msg_image_rect)


class DButton:

    def __init__(self, ai, msg):
        """Initialize button attributes"""
        self.screen = ai.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 200, 50
        # self.button_color = (0, 185, 0)
        self.text_color = (0, 215, 165)
        self.font = pygame.font.Font("Font/font.ttf", 48)

        # The button message needs to be prepped once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect(center=(self.width / 2, self.height / 2))
        self.msg_image_rect.centerx += 540
        self.msg_image_rect.centery += 480

    def draw_button(self):
        # Draw blank button then draw message
        self.screen.blit(self.msg_image, self.msg_image_rect)
