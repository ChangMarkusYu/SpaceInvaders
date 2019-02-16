import pygame
import random
from pygame.sprite import Sprite
from pygame.sprite import Group
from script.spritesheet_functions import color_image


class Barrier(Sprite):
    def __init__(self, ai_settings, screen, pos):
        super().__init__()
        self.screen = screen

        self.rect = pygame.Rect(pos, ai_settings.barrier_sprite_data[0:2])
        self.screen_rect = screen.get_rect()

        self.block_row_num = ai_settings.barrier_block_row_num
        self.block_col_num = ai_settings.barrier_block_col_num
        self.blocks = Group()
        self.__fill_blocks(ai_settings)

    def blitme(self):
        for block in self.blocks:
            block.blitme()

    def __fill_blocks(self, ai_settings):
        width = height = ai_settings.barrier_block_ledge
        for row in range(self.block_row_num):
            for col in range(self.block_col_num):
                new_block = Barrier_Block(self.screen, ai_settings,
                                          (width, height, ai_settings.barrier_sprite_data[2] +
                                           width * col, ai_settings.barrier_sprite_data[3] + height * row))
                new_block.rect.x = self.rect.x + width * col
                new_block.rect.y = self.rect.y + height * row
                self.blocks.add(new_block)


class Barrier_Block(Sprite):
    def __init__(self, screen, ai_settings, sprite_data):
        super().__init__()
        self.screen = screen
        self.image = ai_settings.main_sprite_sheet.get_image(sprite_data)
        color_image(ai_settings.theme_color, self.image)
        self.rect = self.image.get_rect()

        # every block takes certain amount of hit
        self.hp = ai_settings.barrier_block_hp

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def __destory_pixels(self, ai_settings):
        pixel_arr = pygame.PixelArray(self.image)
        for i in range(ai_settings.barrier_block_ledge):
            for j in range(ai_settings.barrier_block_ledge):
                if random.randint(0, ai_settings.barrier_block_hp) < 1:
                    pixel_arr[i, j] = ai_settings.bg_color

    def hit(self, ai_settings):
        self.__destory_pixels(ai_settings)
        self.hp -= 1
