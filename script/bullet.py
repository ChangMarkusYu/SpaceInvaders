import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship):
        super().__init__()
        self.screen = screen
        self.ship = ship

        # crop the main sprite sheet
        self.image = ai_settings.main_sprite_sheet.get_image(
            ai_settings.bullet_sprite_data)
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)

        # decrease player's ammo by 1
        self.ship.ammo -= 1

    def update(self, ai_settings):
        self.y -= ai_settings.bullet_speed_factor
        self.rect.y = self.y

    def __del__(self):
        self.ship.ammo += 1
