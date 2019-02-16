import pygame
import random
from pygame.sprite import Sprite
from script.alien_bullet import Alien_Bullet


class Alien(Sprite):
    def __init__(self, ai_settings, screen, type=1):
        super().__init__()
        self.screen = screen
        self.duration = 0.0
        self.dead = False
        self.disabled = False
        self.step = True
        self.type = type
        self.death_cycle = 0

        # each alien has limited amount of ammo
        self.ammo = ai_settings.alien_ammo

        # crop the main sprite sheet
        self.image = ai_settings.main_sprite_sheet.get_image(
            ai_settings.alien_sprite_data[type])
        self.image_1 = self.image
        self.image_2 = ai_settings.main_sprite_sheet.get_image(
            ai_settings.alien_sprite_data[type + 3])
        self.rect = self.image.get_rect()

        # death sfx
        self.death_sound = pygame.mixer.Sound(ai_settings.alien_death_sfx)
        self.death_sound.set_volume(ai_settings.volume)

        # put the alien on the top left corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height * ai_settings.upper_margin_factor

        self.x = float(self.rect.x)

        # rectangular probe for detecting player/aliens in front of it
        self.probe = pygame.Rect(0, 0, ai_settings.alien_probe_width,
                                 ai_settings.alien_probe_height)
        self.probe.centerx = self.rect.centerx
        self.probe.top = self.rect.top

    def place_corpse(self, ai_settings):
        self.death_sound.play()
        self.image = ai_settings.main_sprite_sheet.get_image(
            ai_settings.alien_sprite_data[7])
        self.rect.width = self.rect.height = 0
        self.dead = True

    def update(self, ai_settings, flag, screen, ship, aliens, alien_bullets):
        if self.disabled or self.dead:
            return

        if not flag:
            self.x += ai_settings.alien_horizontal_movement_distance * \
                ai_settings.alien_direction
            self.rect.x = self.x
            self.probe.x = self.x
        else:
            self.rect.y += ai_settings.alien_vertical_movement_distance
            self.probe.y += ai_settings.alien_vertical_movement_distance

        self.brain(ai_settings, screen, ship, aliens, alien_bullets)

        # movement animation
        if self.step:
            self.image = self.image_2
            self.step = False
        else:
            self.image = self.image_1
            self.step = True

    def disable(self):
        self.disabled = True

    def enable(self):
        self.disabled = False

    def is_out_of_bound(self, ai_settings):
        screen_rect = self.screen.get_rect()
        return self.rect.right + ai_settings.alien_horizontal_movement_distance * \
            ai_settings.alien_direction >= screen_rect.right or self.rect.left + \
            ai_settings.alien_horizontal_movement_distance * \
            ai_settings.alien_direction <= 0

    def is_clear_to_fire(self, ai_settings, aliens, ship):
        if self.ammo <= 0:
            return False
        for alien in aliens:
            if alien is not self and \
                    pygame.Rect.colliderect(self.probe, alien):
                return False
        factor = random.randint(0, 100)
        return factor < ai_settings.alien_fire_probability

    def brain(self, ai_settings, screen, ship, aliens, alien_bullets):
        if self.is_clear_to_fire(ai_settings, aliens, ship):
            new_alien_bullet = Alien_Bullet(ai_settings, screen, self)
            alien_bullets.add(new_alien_bullet)
            self.ammo -= 1
