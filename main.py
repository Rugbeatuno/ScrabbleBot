import pygame
pygame.init()

from visualization import Visualization
import constants as cn

def update_mouse_state(event):
    cn.mouse_pos = pygame.mouse.get_pos()
    cn.clicked = event.type == pygame.MOUSEBUTTONDOWN

def main():
    clock = pygame.time.Clock()
    running = True

    display = Visualization()
    while running:
        for event in pygame.event.get():
            update_mouse_state(event)

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    display.change_travel_direction()
                else:
                    display.get_pressed_key(event.key)


        display.refresh()
        pygame.display.update()
        clock.tick(15)

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()