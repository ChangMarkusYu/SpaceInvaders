import pygame
from script.spritesheet_functions import SpriteSheet
class Settings():
    # A class that stores all settings of Space Invaders
    def __init__(self):
        # screen size and background color
        self.screen_width = 224
        self.screen_height = 256
        self.bg_color = (0,0,0)

        # theme color
        self.theme_color = (0, 255, 0) #'lime green'
        self.saucer_color = (255, 0, 0)

        # master volume
        self.volume = 0.2

        # the main sprite sheet path
        self.main_sprite_sheet = SpriteSheet('res/si_characters.png')
        # high score file path
        self.file_path = "res/hi_score.txt"
        # read high score
        self.high_score = self.read_hi_score()

        # player's ship
        self.ship_speed_factor = 1.5
        self.ship_sprite_data = (13, 8, 36, 18)
        self.ship_ammo = 1
        self.score = 0

        self.ship_hit = False
        self.ship_lives = 3
        self.game_over = False
        self.game_paused = False

        self.ship_fire_sfx = "res/shoot.wav"

        # destoryed ship
        self.ship_destoryed_1 = (16, 8, 53, 18)
        self.ship_destoryed_2 = (16, 8, 69, 18)
        self.ship_death_animation_duration = 2000
        self.ship_death_sfx = "res/explosion.wav"

        # bullet
        self.bullet_speed_factor = 4
        self.bullet_sprite_data = (1, 4, 31, 21)

        # aliens
        self.alien_base_score = 10
        self.alien_speed_factor = 556
        self.alien_bullet_speed_factor = (1.6, 3.2)
        self.alien_ammo = 8
        self.alien_fire_probability = 8

        self.alien_horizontal_movement_distance = 4
        self.alien_vertical_movement_distance = 8
        self.alien_direction = 1
        self.alien_sprite_data = ((16, 8, 2, 4),
                                  (12, 8, 21, 3), (11, 8, 51, 3),(8, 8, 79, 3),
                                  (12, 8, 36, 3), (11, 8, 65, 3), (8, 8, 91, 3),
                                  (13, 8, 102, 3))
        self.alien_bullet_sprite_data = ((3, 7, 100, 19), (3, 1, 89, 22),
                                         (3, 7, 105, 19), (1, 6, 95, 20))

        self.alien_death_sfx = 'res/invaderkilled.wav'

        self.alien_probe_width = 1
        self.alien_probe_height = 256
        self.alien_alignment_width = 12
        self.alien_alignment_height = 8

        # alien fleet formation
        self.upper_margin_factor = 6
        self.side_margin_factor = 2
        self.bottom_margin_factor = 16
        self.horizontal_spacing = 5
        self.vertical_spacing_factor = 2

        # alien death animation
        self.death_cycle = 1

        # kills required for game to speed up
        self.kills = 0
        self.kills_to_speed_up = 18
        self.speed_up_factor = 0.8

        # mystery ship
        self.saucer_appear_kills = 20
        self.saucer_speed = 1
        self.saucer_score = 300
        self.saucer_death_sfx = 'res/ufo_highpitch.wav'
        self.saucer_appear_sfx = 'res/ufo_lowpitch.wav'

        # barrier information
        self.barrier_sprite_data = (24, 18, 5, 14)
        self.barrier_side_margin = 24
        self.barrier_upper_margin = 180
        self.barrier_spacing = 50

        self.barrier_block_hp = 2
        self.barrier_block_ledge = 6
        self.barrier_block_row_num = 3
        self.barrier_block_col_num = 4

        # text sprites - the alphabet
        # 0 ~ 25: letters, 26 ~ 35: numbers, 36 ~ 42: special characters
        self.alphabet_sprite =  ((5, 7, 4, 38), (5, 7, 11, 38), (5, 7, 18, 38),
                                 (5, 7, 25, 38), (5, 7, 32, 38), (5, 7, 39, 38),
                                 (5, 7, 46, 38), (5, 7, 54, 38), (3, 7, 61, 38),
                                 (5, 7, 66, 38), (5, 7, 73, 38), (5, 7, 81, 38),
                                 (5, 7, 87, 38), (5, 7, 4, 51), (5, 7, 11, 51),
                                 (5, 7, 18, 51), (5, 7, 25, 51), (5, 7, 33, 51),
                                 (5, 7, 40, 51), (5, 7, 47, 51), (5, 7, 54, 51),
                                 (5, 7, 62, 51), (5, 7, 69, 51), (5, 7, 77, 51),
                                 (5, 7, 84, 51), (5, 7, 91, 51), (5, 7, 4, 63),
                                 (3, 7, 11, 63), (5, 7, 17, 63), (5, 7, 24, 63),
                                 (5, 7, 31, 63), (5, 7, 38, 63), (5, 7, 45, 63),
                                 (5, 7, 52, 63), (5, 7, 59, 63), (5, 7, 66, 63),
                                 (5, 1, 74, 66), (4, 7, 81, 63), (4, 7, 87, 63),
                                 (5, 7, 93, 63), (5, 7, 100, 63), (5, 3, 107, 65))

        self.character_map = {'-' : 36, '<' : 37, '>' : 38, '*' : 39, '?' : 40, '=' : 41}

        self.text_height = 7
        self.text_padding = 8
        self.text_upper_margin = 10
        self.text_side_margin = 15
        self.line_spacing = 5

        self.screen_upper_border = 40
        self.screen_bottom_border = 40

        self.song_queue = ['res/fastinvader4.wav', 'res/fastinvader1.wav',
                           'res/fastinvader2.wav', 'res/fastinvader3.wav']

    def read_hi_score(self):
        with open(self.file_path) as f:
            high_score = f.read()
        return int(high_score)

    def write_hi_score(self):
        with open(self.file_path, 'w') as f:
            f.write(str(self.score))
