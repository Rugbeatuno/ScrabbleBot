import pygame
pygame.init()

from visualization import Visualization
import constants as cn

def update_mouse_state(event):
    cn.mouse_pos = pygame.mouse.get_pos()
    cn.clicked = event.type == pygame.MOUSEBUTTONUP


def main():
    clock = pygame.time.Clock()
    running = True

    display = Visualization()
    while running:
        for event in pygame.event.get():
            update_mouse_state(event)
            if event.type == pygame.QUIT:
                running = False

            display.refresh(event)
        display.refresh(None)
        pygame.display.update()
        clock.tick(15)

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()