import pygame
import constants as cn



def create_text(window, pos, text, font_size, color=(0, 0, 0)):
    text = str(text)
    x_center, y_center = pos
    font = pygame.font.Font('freesansbold.ttf', font_size)
    string = font.render(text, True, color)
    textRect = string.get_rect()
    textRect.center = (int(x_center), int(y_center))
    window.blit(string, textRect)


