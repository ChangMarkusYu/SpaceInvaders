import pygame

# class used to grab an image out of a spritesheet
class SpriteSheet():
    # load the spritesheet
    def __init__(self, path):
        self.spritesheet = pygame.image.load(path)

    # function that grabs the image
    def get_image(self, image_data, offset = (0,0)):
        image_surface = pygame.Surface(image_data[0:2])
        image_surface.blit(self.spritesheet, offset, (image_data[2:5] + image_data[0:2]))
        image_surface.set_colorkey((0,128, 255))

        return image_surface

    def merge_image(self, image_data_1, image_data_2):
        surface_data = []
        for i in range(2):
            surface_data.append(max(image_data_1[i], image_data_2[i]))
        image_surface = pygame.Surface(tuple(surface_data))

        image_surface.blit(self.spritesheet,(0,1),(image_data_1[2:5] + image_data_1[0:2]))
        image_surface.blit(self.spritesheet,(1,0),(image_data_2[2:5] + image_data_2[0:2]))
        image_surface.set_colorkey((0,128, 255))

        return image_surface

    def generate_text(self, text, ai_settings):
        surface_width = len(text) * (ai_settings.text_padding)
        surface_height = ai_settings.text_height

        image_surface = pygame.Surface((surface_width, surface_height))
        for i in range(len(text)):
            char = text[i]
            if char == " ":
                continue
            else:
                offset_x = 0
                offset_y = 0
                if char.isalpha():
                    if char == 'i':
                        offset_x = 1
                    num = ord(char) - ord('a')
                elif char.isnumeric():
                    if char == '1':
                        offset_x = 1
                    num = ord(char) - ord('0') + 26
                else:
                    if char == '-' or char == '=':
                        offset_y = 3
                    num = ai_settings.character_map[char]
                image_surface.blit(self.spritesheet,
                                   (i * ai_settings.text_padding + offset_x, offset_y),
                                   ai_settings.alphabet_sprite[num][2:5] +
                                   ai_settings.alphabet_sprite[num][0:2])

        image_surface.set_colorkey((0,128, 255))

        return image_surface

def color_image(color, *surfaces):
    for surface in surfaces:
        colorkey = surface.get_colorkey()
        pixel_arr = pygame.PixelArray(surface)
        rect = surface.get_rect()
        for i in range(rect.width):
            for j in range(rect.height):
                if pixel_arr[i][j] != surface.map_rgb(colorkey):
                    pixel_arr[i][j] = color

def concatenate_surface_x(surfaces):
    max_height = max_width = 0
    last_width = 0
    for surface in surfaces:
        if surface.get_height() > max_height:
            max_height = surface.get_height()
        max_width += surface.get_width()

    result_surface = pygame.Surface((max_width, max_height))
    for surface in surfaces:
        result_surface.blit(surface, (last_width,0))
        last_width += surface.get_width()

    return result_surface

def concatenate_surface_y(surfaces, spacing):
    max_height = max_width = 0
    last_height = 0
    for surface in surfaces:
        if surface.get_width() > max_width:
            max_width = surface.get_width()
        max_height += (surface.get_height() + spacing)

    result_surface = pygame.Surface((max_width, max_height))
    for surface in surfaces:
        offset = (max_width - surface.get_width())/2
        result_surface.blit(surface, (offset,last_height))
        last_height += (surface.get_height() + spacing)

    return result_surface
