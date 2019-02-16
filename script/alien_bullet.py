import pygame
import random
from script.bullet import Bullet


class Alien_Bullet(Bullet):
    def __init__(self, ai_settings, screen, alien):
        super().__init__(ai_settings, screen, alien)

        # crop the main sprite sheet
        self.type = random.randint(0, 1)
        if self.type == 0:
            self.image = ai_settings.main_sprite_sheet.get_image(
                ai_settings.alien_bullet_sprite_data[self.type])

            self.image_2 = ai_settings.main_sprite_sheet.get_image(
                ai_settings.alien_bullet_sprite_data[self.type + 2])
        else:
            self.image = ai_settings.main_sprite_sheet.merge_image(
                ai_settings.alien_bullet_sprite_data[self.type],
                ai_settings.alien_bullet_sprite_data[self.type + 2])

            self.image_2 = pygame.transform.rotate(self.image, 180)

        self.image_1 = self.image

        self.rect = self.image.get_rect()
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.top

        self.speed = ai_settings.alien_bullet_speed_factor[random.randint(
            0, 1)]
        self.flag = False

    def update(self, ai_settings):
        self.y += self.speed
        self.rect.y = self.y
        # Bullet animation
        if self.flag:
            self.image = self.image_1
            self.flag = False
        else:
            self.image = self.image_2
            self.flag = True
