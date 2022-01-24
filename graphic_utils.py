import pygame
import constants as cn


fonts = {}
def create_text(window, pos, text, font_size, color=(0, 0, 0)):
    text = str(text)
    x_center, y_center = pos
    font = get_font(font_size)
    string = font.render(text, True, color)
    textRect = string.get_rect()
    textRect.center = (int(x_center), int(y_center))
    window.blit(string, textRect)

def get_font(font_size):
    if font_size in fonts:
        return fonts[font_size]
    fonts[font_size] = pygame.font.Font('freesansbold.ttf', font_size)
    return fonts[font_size]
